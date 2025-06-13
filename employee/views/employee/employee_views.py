from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator

from employee.models import Employee
from employee.forms import EmployeeForm, UpdateEmployeeForm 
from employee.utils.delete_attention import send_delete_warning


def employee_create(request):
    """View to create a new employee."""
    department = request.GET.get('department') or request.session.get('department')

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(initial={'department': department})

    return render(
        request, 
        'employee/employee_create.html', 
        {
            'form': form,
            'object_type': 'Employee',
            'selected_department': department,
            'cancel_url': reverse('employee_list'),

        }
    )


def employee_list(request):
    """View to list all employees with filtering and pagination."""
    employees = Employee.objects.all()

    # Filtering
    department = request.GET.get('department') or request.session.get('department')
    employee_id = request.GET.get('employee_id')
    employee_name = request.GET.get('employee_name')
    job_title = request.GET.get('job_title')

    if department:
        employees = employees.filter(department=department)
    if employee_id:
        employees = employees.filter(employee_id=employee_id)
    if employee_name:
        employees = employees.filter(name__icontains=employee_name)
    if job_title:
        employees = employees.filter(job_title=job_title)

    # Get distinct job titles for filtering
    if department:
        job_titles = (
            Employee.objects.filter(department=department)
            .values_list('job_title', flat=True)
            .distinct()
        )
    else:
        job_titles = Employee.objects.values_list('job_title', flat=True).distinct()

    # Ensure consistent ordering for pagination
    employees = employees.order_by('employee_id')
    
    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

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


def employee_update(request, pk):
    """View to update an existing employee."""
    employee = get_object_or_404(Employee, pk=pk)
    department = request.GET.get('department') or request.session.get('department')

    if request.method == 'POST':
        form = UpdateEmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = UpdateEmployeeForm(instance=employee)

    return render(
        request,
        'employee/employee_update.html',
        {
            'form': form,
            'object_type': 'Employee',
            'object_name': f"{employee.employee_id}/{employee.name}",
            'selected_department': department,
            'cancel_url': reverse('employee_list'),
        }
    )


def employee_delete(request, pk):
    """View to delete an employee."""
    employee = get_object_or_404(Employee, pk=pk)
    #department = request.GET.get('department') or request.session.get('department')

    if request.method == "POST":
        object_name = f"{employee.employee_id}/{employee.name}"
        employee.delete()
        send_delete_warning(request, object_name)

        return redirect('employee_list')
