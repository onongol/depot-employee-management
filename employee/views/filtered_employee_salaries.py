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

    employees = Employee.objects.prefetch_related('monthlysalary_set').all()
    
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
        for monthly_salary in employee.monthlysalary_set.all():
            if (month and str(monthly_salary.month) != month) or (year and str(monthly_salary.year) != year):
                continue
            total_piecework_amount = Piecework.objects.filter(
                employee=employee,
                work_date__month=monthly_salary.month,
                work_date__year=monthly_salary.year
            ).aggregate(total_amount=Sum('amount_price'))['total_amount'] or 0
            employee_salaries.append(
                {
                    'employee': employee,
                    'monthly_salary': monthly_salary,
                    'total_piecework_amount': round(total_piecework_amount, 2),
                    'total_salary': round(
                        monthly_salary.salary_month + total_piecework_amount, 2
                    ),
                }
            )

    return employee_salaries
