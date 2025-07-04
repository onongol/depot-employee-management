from django.shortcuts import render
from django.db.models import Sum

from employee.models import Employee
from employee.models import DailySalary
from .employee_salary_filtered import employee_salaries_prepare
from employee.utils.select_department import get_selected_department
from employee.utils.filters import filter_employees
from employee.utils.filters import filter_month_year
from employee.utils.pagination import paginate_queryset


def employee_salary_list(request):
    """View to list all employee salaries with filters and pagination."""
    # Prepare the base queryset and filter parameters
    employees, employee_id, employee_name, department, job_title, month, year, current_year = employee_salaries_prepare(request)

    # Get the selected department from the request
    department = get_selected_department(request)

    # Only active employees
    employees = employees.filter(is_active=True)

    # Get all unique job titles that exist in DailySalary for filter dropdown
    job_titles = (
        Employee.objects.filter(department=department, dailysalary__isnull=False)
        .values_list('job_title', flat=True)
        .distinct()
        )
    
    # Prepare months and years for filter dropdowns
    months = [i for i in range(1, 13)]
    years = [d.year for d in DailySalary.objects.dates('salary_date', 'year')]

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
                    'department': employee.department,
                    'month': group_month,
                    'year': group_year,
                    'total_salary_day': round(total_salary_day, 2),
                    'total_piecework_amount': round(total_piecework_amount, 2),
                    'total_salary': total_salary,
                }
            )

    # Handle sorting based on query parameters
    order_by = request.GET.get('order_by')
    direction = request.GET.get('direction')
    
    if order_by in ['employee_id', 'month', 'year']:
        reverse = direction == 'desc'
        if order_by == 'employee_id':
            # Sort by employee_id
            employee_salaries.sort(
                key=lambda x: x['employee'].employee_id, reverse=reverse
            )
        else:
            # Sort by year and month
            employee_salaries.sort(
                key=lambda x: ( x['year'], x['month']), reverse=reverse
            )
    else:
        # Default sorting by year and month, descending
        employee_salaries.sort(
            key=lambda x: (x['year'], x['month']), reverse=True
        )

    # Paginate the results (10 per page)
    page_obj = paginate_queryset(request, employee_salaries)

    # Render the template with all context data
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
            'months': months,
            'years': years,
            'current_year': current_year,
            'page_obj': page_obj,
            'selected_department': department,
        }
    )
