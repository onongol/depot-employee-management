from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from employee.models import Employee
from employee.models import DailySalary
from employee.views.employee_salary.employee_salary_calculate import employee_salary_calculate
from .employee_salary_filtered import employee_salaries_prepare
from employee.utils.select_department import get_selected_department
from employee.utils.filters import filter_employees
from employee.utils.pagination import paginate_queryset
from employee.utils.selects import get_distinct_values


@login_required(login_url='login')
def employee_salary_list(request):
    """View to list all employee salaries with filters and pagination."""
    # Prepare the base queryset and filter parameters
    employees, employee_id, employee_name, department, job_title, month, year, current_year = employee_salaries_prepare(request)

    # Get the selected department from the request
    department = get_selected_department(request)

    # Only active employees
    if request.user.groups.filter(name='Employees').exists():
        employees = employees.filter(user=request.user, is_active=True)
    else:
        employees = employees.filter(is_active=True)

    # Get all unique job titles that exist in DailySalary for filter dropdown
    job_titles = get_distinct_values(Employee, 'job_title', department, department_field='department', only_with_salary=True)

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
    
    # Calculate salaries for the filtered employees using the shared function
    employee_salaries = employee_salary_calculate(employees, month, year)

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
                key=lambda x: (x['year'], x['month']), reverse=reverse
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
