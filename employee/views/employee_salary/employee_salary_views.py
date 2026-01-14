from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS, GROUP_WAGON
from employee.models import Employee
from employee.utils.filters import filter_employees
from employee.utils.pagination import paginate_queryset
from employee.utils.selects import get_distinct_values
from employee.views.employee_salary.employee_salary_calculate import employee_salary_calculate
from employee.views.employee_salary.employee_salary_prepare import employee_salaries_prepare
from employee.views.employee_salary.employee_salary_sort import apply_ordering


@login_required(login_url='login')
def employee_salary_list(request):
    """View to list all employee salaries with filters and pagination."""
    (
        employees, 
        employee_id, 
        employee_name, 
        department, 
        job_title,
        wagon_number, 
        month, 
        year, 
        month_period, 
        group,
        order_by,
        direction
    ) = employee_salaries_prepare(request)

    # Populate the job_title filter dropdown with distinct titles (scoped to the selected department and only employees with salary data).
    job_titles = get_distinct_values(
        Employee, 
        'job_title', 
        department, 
        department_field='department', 
        only_with_salary=True
    )

    employees = filter_employees(
        employees, 
        department=department, 
        employee_id=employee_id, 
        employee_name=employee_name, 
        job_title=job_title
    )
    
    # Enable wagon-level grouping only when the user selected the "wagon" group and the department supports wagon tracking.
    group_by_wagon = (group == GROUP_WAGON) and (department in ALLOWED_WAGON_DEPARTMENTS)

    employee_salaries = employee_salary_calculate(
        employees, 
        month, 
        year, 
        group_by_wagon=group_by_wagon,
        wagon_number=wagon_number if group_by_wagon else None
    )
       
    apply_ordering(
        employee_salaries,
        order_by,
        direction,
        allowed_fields=["employee_id", "month", "year"],
    )

    page_obj = paginate_queryset(request, employee_salaries)

    filters = {
        'employee_id': employee_id,
        'employee_name': employee_name,
        'department': department,
        'job_title': job_title,
        'wagon_number': wagon_number,
        'month': month,
        'year': year,
        'month_period': month_period,
        'group': group
    }

    return render(
        request,
        'employee_salary/employee_salary_list.html',
        {   
            'ALLOWED_WAGON_DEPARTMENTS': ALLOWED_WAGON_DEPARTMENTS,
            'GROUP_WAGON': GROUP_WAGON,
            'employee_salaries': page_obj,
            'job_titles': job_titles,
            'page_obj': page_obj,
            'selected_department': department,
            'filters': filters,
            'group': group
        }
    )
