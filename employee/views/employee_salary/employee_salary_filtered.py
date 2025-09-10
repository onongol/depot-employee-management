from django.db.models import Sum
from collections import defaultdict
from datetime import datetime

from employee.models import Employee
from employee.models import DailySalary
from employee.utils.filters import filter_employees, filter_month_year


def employee_salaries_prepare(request):
    """Prepare the base queryset and filter parameters for employee salaries."""
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
    if request.user.groups.filter(name='Employees').exists():
        # If the user is an employee, filter only their record
        employees = Employee.objects.prefetch_related('dailysalary_set').filter(user=request.user, is_active=True)
    else:
        # Otherwise, get all active employees
        employees = Employee.objects.prefetch_related('dailysalary_set').filter(is_active=True)

    return employees, employee_id, employee_name, department, job_title, month, year, current_year


def employee_salary_calculate(employees, month, year):
    """Calculate employee salaries based on daily salary records using aggregation."""
    # Fetch all DailySalary records for selected employees and period in a single query
    salary_groups = DailySalary.objects.filter(employee__in=employees)
    salary_groups = filter_month_year(salary_groups, month=month, year=year)
    # Aggregate total salary_day per employee per month and year
    salary_groups = (
        salary_groups
        .values('employee', 'salary_date__year', 'salary_date__month')
        .annotate(total_salary_day=Sum('salary_day'))
    )

    # Group salary data by employee
    salary_data = defaultdict(list)
    for group in salary_groups:
        salary_data[group['employee']].append(group)

    employee_salaries = []
    for employee in employees:
        for group in salary_data.get(employee.employee_id, []):
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


def get_filtered_employee_salaries(request):
    """Return a list of filtered employee salaries based on request parameters."""
    # Prepare the base queryset and filter parameters
    employees, employee_id, employee_name, department, job_title, month, year, current_year = employee_salaries_prepare(request)

    # Apply filters to the employee queryset using reusable filter functions
    employees = filter_employees(
        employees, 
        department=department, 
        employee_id=employee_id, 
        employee_name=employee_name, 
        job_title=job_title
    )

    # Calculate salaries for the filtered employees
    employee_salaries = employee_salary_calculate(employees, month, year)

    return employee_salaries
