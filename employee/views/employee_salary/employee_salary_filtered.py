from django.db.models import Sum
from datetime import datetime

from employee.models import Employee
from employee.utils.filters import filter_employees
from employee.utils.filters import filter_month_year


def get_filtered_employee_salaries(request):
    """Return a list of filtered employee salaries based on request parameters."""
    # Get the current year for default filtering
    current_year = datetime.now().year

    # Extract filter parameters from the request
    employee_id = request.GET.get('employee_id', '')    
    employee_name = request.GET.get('employee_name', '')
    department = request.GET.get('department', '')
    job_title = request.GET.get('job_title', '')
    month = request.GET.get('month', '')
    year = request.GET.get('year', str(current_year))

    # Query all employees and prefetch related DailySalary data for efficiency
    employees = Employee.objects.prefetch_related('dailysalary_set').all()
    
    # Apply filters to the employee queryset using reusable filter functions
    employees = filter_employees(
        employees, 
        department=department, 
        employee_id=employee_id, 
        employee_name=employee_name, 
        job_title=job_title
    )

    # Prepare the data for the template
    employee_salaries = []
    for employee in employees:
        # Filter daily salaries by month and year if provided
        daily_salaries = employee.dailysalary_set.all()
        daily_salaries = filter_month_year(daily_salaries, month=month, year=year)

        # Group daily salaries by month and year, and sum salary_day for each group
        grouped = (
            daily_salaries
            .values('salary_date__year', 'salary_date__month')
            .annotate(
                total_salary_day=Sum('salary_day'),
            )
        )

        # For each group (month/year), calculate total salary and piecework
        for group in grouped:
            group_month = group['salary_date__month']
            group_year = group['salary_date__year']

            # Use model methods to calculate salary components for this period
            total_salary_day = employee.get_total_salary_day(group_month, group_year)
            total_piecework_amount = employee.get_total_piecework_amount(group_month, group_year)
            total_salary = employee.get_total_salary(group_month, group_year)

            # Append the calculated data to the result list
            employee_salaries.append(
                {
                    'employee': employee,
                    'month': group_month,
                    'year': group_year,
                    'total_salary_day': round(total_salary_day, 2),
                    'total_piecework_amount': round(total_piecework_amount, 2),
                    'total_salary': total_salary,
                }
            )

    return employee_salaries
