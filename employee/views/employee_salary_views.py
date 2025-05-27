from django.shortcuts import render
from django.db.models import Sum
from django.core.paginator import Paginator
from datetime import datetime

from employee.models import Employee
from employee.models import Piecework
from employee.models import MonthlySalary


def employee_salary_list(request):
    """View to list all employee salaries with filters and pagination."""
    MONTH_CHOICES = [
        (1, '01'), (2, '02'), (3, '03'), (4, '04'),
        (5, '05'), (6, '06'), (7, '07'), (8, '08'),
        (9, '09'), (10, '10'), (11, '11'), (12, '12'),
    ]
    current_year = datetime.now().year

    # Filtering
    employee_id = request.GET.get('employee_id', '')    
    employee_name = request.GET.get('employee_name', '')
    department = request.GET.get('department', '')
    job_title = request.GET.get('job_title', '')
    month = request.GET.get('month', '')  # Default to current month
    year = request.GET.get('year', str(current_year))  # Default to current year

    # Query Employee and prefetch related MonthlySalary data
    employees = Employee.objects.prefetch_related('monthlysalary_set').all()

    # Get all unique department names that exist in Employee Salary
    departments = (
        Employee.objects.filter(monthlysalary__isnull=False)
        .values_list('department', flat=True)
        .distinct()
    )
    # Get all unique job titles that exist in Employee Salary
    job_titles = (
        Employee.objects.filter(monthlysalary__isnull=False)
        .values_list('job_title', flat=True)
        .distinct()
    )
    # Get all unique years that exist in MonthlySalary
    years = (
        MonthlySalary.objects.values_list('year', flat=True).distinct()
    )

    # Apply filters
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
            # Apply month and year filters to MonthlySalary
            if (month and str(monthly_salary.month) != month) or (year and str(monthly_salary.year) != year):
                continue

            # Sum up all piecework amounts for the employee in the given month and year
            total_piecework_amount = Piecework.objects.filter(
                employee=employee,
                work_date__month=monthly_salary.month,
                work_date__year=monthly_salary.year
            ).aggregate(total_amount=Sum('amount_price'))['total_amount'] or 0  # Default to 0 if no piecework

            # Add the employee's salary data to the list
            employee_salaries.append(
                {
                    'employee': employee,
                    'monthly_salary': monthly_salary,
                    'total_piecework_amount': round(total_piecework_amount, 2),
                    'total_salary': round(monthly_salary.salary_month + total_piecework_amount, 2),  # Example calculation
                }
            )
    
    # Handle sorting
    order_by = request.GET.get('order_by')
    direction = request.GET.get('direction')

    if order_by:
        reverse = direction == 'desc'
        if order_by == 'employee_id':
            employee_salaries.sort(
                key=lambda x: x['employee'].employee_id, reverse=reverse
            )
        if order_by == 'month':
            employee_salaries.sort(
                key=lambda x: x['monthly_salary'].month, reverse=reverse
            )
        elif order_by == 'year':
            employee_salaries.sort(
                key=lambda x: x['monthly_salary'].year, reverse=reverse
            )

    # Paginate the queryset
    paginator = Paginator(employee_salaries, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)    

    return render(
        request, 
        'employee_salary/employee_salary_list.html', 
        {
            'employee_salaries': page_obj,
            'filters': {
                'employee_id': employee_id,
                'employee_name': employee_name,
                'department': department,
                'job_title': job_title,
                'month': month,
                'year': year,
            },
            'departments': departments,
            'job_titles': job_titles,
            'MONTH_CHOICES': MONTH_CHOICES,
            'years': years,
            'current_year': current_year,
            'page_obj': page_obj,
        }
    )
