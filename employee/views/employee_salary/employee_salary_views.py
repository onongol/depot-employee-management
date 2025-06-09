from django.shortcuts import render
from django.db.models import Sum
from django.core.paginator import Paginator
from datetime import datetime

from employee.models import Employee
from employee.models import Piecework
from employee.models import DailySalary


def employee_salary_list(request):
    """View to list all employee salaries with filters and pagination."""
    MONTH_CHOICES = [
        (1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06'),
        (7, '07'), (8, '08'), (9, '09'), (10, '10'), (11, '11'), (12, '12'),
    ]

    # Get the current year for default filtering
    current_year = datetime.now().year

    # Filtering
    department = request.GET.get('department') or request.session.get('department')
    employee_id = request.GET.get('employee_id', '')    
    employee_name = request.GET.get('employee_name', '')
    job_title = request.GET.get('job_title', '')
    month = request.GET.get('month', '')
    year = request.GET.get('year', str(current_year))

    # Query Employee and prefetch related DailySalary data
    employees = Employee.objects.prefetch_related('dailysalary_set').all()

    # Get all unique job titles that exist in DailySalary
    if department:
        job_titles = (
            Employee.objects.filter(department=department, dailysalary__isnull=False)
            .values_list('job_title', flat=True)
            .distinct()
        )
    else:
        job_titles = (
            Employee.objects.filter(dailysalary__isnull=False)
            .values_list('job_title', flat=True)
            .distinct()
        )

    # Get all unique years that exist in DailySalary
    years = [d.year for d in DailySalary.objects.dates('salary_date', 'year')]

    # Apply filters
    if department:
        employees = employees.filter(department__icontains=department)
    if employee_id:
        employees = employees.filter(employee_id__exact=employee_id)
    if employee_name:
        employees = employees.filter(name__icontains=employee_name)
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
        
        # Iterate through the grouped data to calculate total salaries
        for group in grouped:
            group_month = group['salary_date__month']
            group_year = group['salary_date__year']

            # Sum up all piecework amounts for the employee in the given month and year
            total_piecework_amount = Piecework.objects.filter(
                employee=employee,
                work_date__month=group_month,
                work_date__year=group_year
            ).aggregate(total_amount=Sum('amount_price'))['total_amount'] or 0

            employee_salaries.append(
                {
                    'employee': employee,
                    'department': employee.department,
                    'month': group_month,
                    'year': group_year,
                    'total_salary_day': round(group['total_salary_day'] or 0, 2),
                    'total_piecework_amount': round(total_piecework_amount, 2),
                    'total_salary': round((group['total_salary_day'] or 0) + total_piecework_amount, 2),
                }
            )

    # Handle sorting
    order_by = request.GET.get('order_by')
    direction = request.GET.get('direction')
    
    if order_by in ['employee_id', 'month', 'year']:
        reverse = direction == 'desc'
        if order_by == 'employee_id':
            employee_salaries.sort(
                key=lambda x: x['employee'].employee_id, reverse=reverse
            )
        else:
            employee_salaries.sort(
                key=lambda x: (x['month'], x['year']), reverse=reverse
            )
    else:
        # Default sorting by employee_id
        employee_salaries.sort(
            key=lambda x: (x['month'], x['year']), reverse=True
        )

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
            'job_titles': job_titles,
            'MONTH_CHOICES': MONTH_CHOICES,
            'years': years,
            'current_year': current_year,
            'page_obj': page_obj,
            'selected_department': department,
        }
    )
