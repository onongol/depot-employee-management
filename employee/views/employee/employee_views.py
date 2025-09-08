from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test


from employee.mixins.context_mixins import EmployeeContextMixin
from employee.mixins.delete_warning_mixins import DeleteWarningMixin
from employee.mixins.delete_warning_mixins import DeleteProtectionMixin
from employee.models import Employee
from employee.models import DailySalary
from employee.forms import EmployeeForm, UpdateEmployeeForm 
from employee.utils.select_department import get_selected_department
from employee.utils.filters import filter_employees
from employee.utils.pagination import paginate_queryset
from employee.utils.permissions import is_admin, OnlyAdminMixin


class EmployeeCreateView(LoginRequiredMixin, OnlyAdminMixin, EmployeeContextMixin, CreateView):
    login_url = 'login'
    form_class = EmployeeForm
    template_name = "employee/employee_create.html"


class EmployeeUpdateView(LoginRequiredMixin, OnlyAdminMixin, EmployeeContextMixin, UpdateView):
    login_url = 'login'
    form_class = UpdateEmployeeForm
    template_name = "employee/employee_update.html"


class EmployeeDeleteView(LoginRequiredMixin, OnlyAdminMixin, EmployeeContextMixin, DeleteProtectionMixin, DeleteView):
    login_url = 'login'
    template_name = "employee/employee_confirm_delete.html"

    # Get related daily salary records to check if deletion is allowed.
    def get_related_objects(self):
        return DailySalary.objects.filter(employee=self.object)

    def get_block_message(self):
        return (
            f"Cannot delete {self.object.employee_id}/{self.object.name} because it is associated with daily salary and piecework records. "
            "Please remove the related daily salary and piecework records first."
        )

    def get_redirect_url(self):
        return self.success_url

    def get_object_name(self):
        return f"{self.object.employee_id}/{self.object.name}"


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
    job_titles = (
        Employee.objects.filter(department=department)
        .values_list('job_title', flat=True)
        .distinct()
        )
    
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


@user_passes_test(is_admin, login_url='login')
@login_required(login_url='login')
def employee_activate(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.is_active = True
    employee.save()
    # Activate related records if needed
    return redirect(reverse('employee_list'))


@user_passes_test(is_admin, login_url='login')
@login_required(login_url='login')
def employee_deactivate(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.is_active = False
    employee.save()
    # Deactivate related records if needed
    return redirect(reverse('employee_list'))
