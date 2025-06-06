from django.db.models import Sum
from datetime import datetime

from employee.models import Employee, Piecework


def get_filtered_employee_salaries(request):
    """Return a list of filtered employee salaries based on request parameters."""
    current_year = datetime.now().year

    # Filtering
    employee_id = request.GET.get('employee_id', '')    
    employee_name = request.GET.get('employee_name', '')
    department = request.GET.get('department', '')
    job_title = request.GET.get('job_title', '')
    month = request.GET.get('month', '')
    year = request.GET.get('year', str(current_year))

    employees = Employee.objects.prefetch_related('dailysalary_set').all()
    
    if employee_id:
        employees = employees.filter(employee_id__exact=employee_id)
    if employee_name:
        employees = employees.filter(name__icontains=employee_name)
    if department:
        employees = employees.filter(department__icontains=department)
    if job_title:
        employees = employees.filter(job_title__icontains=job_title)

    # Prepare the data for the template
    employee_salaries = []
    for employee in employees:
        # Filter daily salaries by month and year if provided
        daily_salaries = employee.dailysalary_set.all()
        if month:
            daily_salaries = daily_salaries.filter(salary_date__month=month)
        if year:
            daily_salaries = daily_salaries.filter(salary_date__year=year)

        # Group by month and year, sum salary_day
        grouped = (
            daily_salaries
            .values('salary_date__year', 'salary_date__month')
            .annotate(
                total_salary_day=Sum('salary_day'),
            )
        )
        for group in grouped:
            group_month = group['salary_date__month']
            group_year = group['salary_date__year']

            total_piecework_amount = Piecework.objects.filter(
                employee=employee,
                work_date__month=group_month,
                work_date__year=group_year
            ).aggregate(total_amount=Sum('amount_price'))['total_amount'] or 0

            employee_salaries.append(
                {
                    'employee': employee,
                    'month': group_month,
                    'year': group_year,
                    'total_salary_day': round(group['total_salary_day'] or 0, 2),
                    'total_piecework_amount': round(total_piecework_amount, 2),
                    'total_salary': round((group['total_salary_day'] or 0) + total_piecework_amount, 2),
                }
            )

    return employee_salaries
