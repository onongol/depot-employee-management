from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _

from employee.models import Employee
from employee.utils.select_department import get_selected_department
from employee.utils.filters import filter_employees
from employee.utils.pagination import paginate_queryset
from employee.utils.selects import get_distinct_values


@login_required(login_url='login')
def employee_list(request):    
    """View to list employees. Workers see only their own record."""
    if request.user.groups.filter(name='Employees').exists():
        employees = Employee.objects.filter(user=request.user)
    else:
        employees = Employee.objects.all()

    # Extract filter parameters from the request
    department = get_selected_department(request)
    employee_id = request.GET.get('employee_id')
    employee_name = request.GET.get('employee_name')
    job_title = request.GET.get('job_title')

    # Filtering logic: apply all filters using a reusable filter function
    employees = filter_employees(employees, department, employee_id, employee_name, job_title)

    # Get distinct job titles for filtering dropdown
    job_titles = get_distinct_values(Employee, 'job_title', department, department_field='department')

    # Ensure consistent ordering for pagination
    employees = employees.order_by('employee_id')
    
    # Paginate the results, 10 records per page
    page_obj = paginate_queryset(request, employees)

    return render(
        request,
        'employee/employee_list.html',
        {
            'employees': page_obj,
            'page_obj': page_obj,
            'job_titles': job_titles,
            'selected_department': department,
        }
    )
