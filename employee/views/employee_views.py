from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator

from employee.models import Employee
from employee.forms import EmployeeForm, UpdateEmployeeForm 
from employee.views.delete_attention import send_delete_warning


def create_employee(request):
    """View to create a new employee."""
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(
        request, 
        'employee/create_employee.html', 
        {
            'form': form,
            'object_type': 'Employee',
            'cancel_url': reverse('employee_list'),
        }
    )


def employee_list(request):
    """View to list all employees with filtering and pagination."""
    employees = Employee.objects.all()

    # Filtering
    employee_id = request.GET.get('employee_id')
    employee_name = request.GET.get('employee_name')
    department = request.GET.get('department')
    job_title = request.GET.get('job_title')

    if employee_id:
        employees = employees.filter(employee_id=employee_id)
    if employee_name:
        employees = employees.filter(name__icontains=employee_name)
    if department:
        employees = employees.filter(department=department)
    if job_title:
        employees = employees.filter(job_title=job_title)

    # For filter dropdowns
    departments = Employee.objects.values_list('department', flat=True).distinct()
    job_titles = Employee.objects.values_list('job_title', flat=True).distinct()

    # Paginate the queryset
    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'employee/employee_list.html',
        {
            'employees': page_obj,
            'page_obj': page_obj,
            'departments': departments,
            'job_titles': job_titles,
        }
    )


def update_employee(request, pk):
    """View to update an existing employee."""
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = UpdateEmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = UpdateEmployeeForm(instance=employee)
    return render(
        request,
        'employee/update_employee.html',
        {
            'form': form,
            'object_type': 'Employee',
            'object_name': f"{employee.employee_id} {employee.name}",
            'cancel_url': reverse('employee_list'),
        }
    )


def delete_employee(request, pk):
    """View to delete an employee."""
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        object_name = f"{employee.employee_id} {employee.name}"
        employee.delete()
        send_delete_warning(request, object_name)
        return redirect('employee_list')
