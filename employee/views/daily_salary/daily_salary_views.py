from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import UpdateView, DeleteView
from django.db import transaction
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test

from employee.mixins.context_mixins import DailySalaryContextMixin
from employee.mixins.delete_warning_mixins import DeleteWarningMixin
from employee.mixins.delete_warning_mixins import DeleteProtectionMixin
from employee.models import Employee
from employee.models import DailySalary
from employee.models import Piecework
from employee.forms import DailySalaryForm, UpdateDailySalaryForm
from employee.utils.select_department import get_selected_department
from employee.utils.filters import filter_daily_salaries
from employee.utils.pagination import paginate_queryset
from employee.utils.converting_date import parse_date
from employee.utils.permissions import is_admin, OnlyAdminMixin, is_creater, OnlyCreaterMixin


class DailySalaryUpdateView(LoginRequiredMixin, OnlyAdminMixin, DailySalaryContextMixin, UpdateView):
    login_url = 'login'
    form_class = UpdateDailySalaryForm
    template_name = "daily_salary/daily_salary_update.html"


class DailySalaryDeleteView(LoginRequiredMixin, OnlyAdminMixin, DailySalaryContextMixin, DeleteProtectionMixin, DeleteView):
    login_url = 'login'
    template_name = "daily_salary/daily_salary_confirm_delete.html"

    # Get related piecework records to check if deletion is allowed.
    def get_related_objects(self):
        return Piecework.objects.filter(
            employee=self.object.employee,
            work_date=self.object.salary_date
        )
    
    def get_block_message(self):
        return (
            f"Cannot delete {self.object.employee.employee_id}/{self.object.employee.name}/{self.object.salary_date} because it is associated with piecework records. Please remove the piecework records first."
        )
    
    # Handle the deletion and send a warning.
    def get_redirect_url(self):
        return self.success_url
    
    def get_object_name(self):
        return (
            f"{self.object.employee.employee_id}/{self.object.employee.name}/{self.object.salary_date}"
        )


@user_passes_test(is_creater, login_url='login')
@login_required(login_url='login')
def daily_salary_create(request):
    """View to create daily salary records for multiple employees, filtered by department."""
    department = get_selected_department(request)

    # Filter employees by selected department, or show none if not selected
    employees = Employee.objects.none()
    if department:
        employees = Employee.objects.filter(department=department, is_active=True)  # Only active employees

    # Ensure consistent ordering for pagination or display
    employees = employees.order_by('employee_id')
    
    errors = []

    if request.method == 'POST':
        selected_ids = request.POST.getlist('employee_ids')
        salary_date = request.POST.get('salary_date')
        hours_per_day = request.POST.get('hours_per_day')

        # Check if any employees are selected
        if not selected_ids:
            errors.append("Please select at least one employee.")

        # Validate required fields
        if not salary_date or not hours_per_day:
            errors.append("Please select date and hours!")

        # Validate required fields
        if not errors:
            try:
                # Use atomic transaction to ensure all records are created together
                with transaction.atomic():
                    for emp_id in selected_ids:
                        # Check for duplicate daily salary record for the same employee and date
                        exists = DailySalary.objects.filter(
                            employee_id=emp_id,
                            salary_date=salary_date
                        ).first()
                        if exists:
                            emp = Employee.objects.get(employee_id=emp_id)
                            errors.append(
                                f"Daily salary record for Employee: {emp_id}/{emp.name} on {salary_date} already exists!"
                            )
                        else:
                            # Create new DailySalary record
                            DailySalary.objects.create(
                                employee_id=emp_id,
                                salary_date=salary_date,
                                hours_per_day=hours_per_day,
                            )
            except Exception as e:
                errors.append(f"Error creating daily salary records: {str(e)}")
        # If no errors, redirect to the list page for the selected department
        if not errors:
            return redirect(f"{reverse('daily_salary_list')}?department={department}")

    return render(
        request,
        'daily_salary/daily_salary_create.html',
        {
            'form': DailySalaryForm(),
            'object_type': 'Daily Salary',
            'employees': employees,
            'errors': errors,
            'today': timezone.now().date(),
            'selected_department': department,
            'cancel_url': reverse('daily_salary_list'),
        }
    )


@login_required(login_url='login')
def daily_salary_list(request):
    """View to list all daily salaries with filtering and pagination."""
    department = get_selected_department(request)

    # Filter daily salaries by department 
    if request.user.groups.filter(name='Employees').exists():
        daily_salaries = DailySalary.objects.filter(employee__user=request.user, employee__department=department, employee__is_active=True)
    else:
        # If not an employee, show all daily salaries in the department 
        daily_salaries = DailySalary.objects.filter(employee__department=department, employee__is_active=True)

    # Filtering by employee ID, name, salary date, and record date
    employee_id = request.GET.get('employee_id')
    employee_name = request.GET.get('employee_name')
    salary_date = parse_date(request.GET.get('salary_date'))
    record_date = parse_date(request.GET.get('record_date'))

    # Apply filters to the daily salaries queryset using reusable filter functions
    daily_salaries = filter_daily_salaries(
        daily_salaries, 
        employee_id=employee_id, 
        employee_name=employee_name, 
        salary_date=salary_date, 
        record_date=record_date
    )

    # Sorting logic: allows sorting by salary_date or record_date, default is by record_date descending
    order_by = request.GET.get('order_by')
    direction = request.GET.get('direction')

    if order_by in ['salary_date', 'record_date']:
        if direction == 'desc':
            daily_salaries = daily_salaries.order_by(f'-{order_by}')
        else:
            daily_salaries = daily_salaries.order_by(order_by)
    else:
        daily_salaries = daily_salaries.order_by('-record_date')

    # Paginate the results, 10 records per page
    page_obj = paginate_queryset(request, daily_salaries)

    return render(
        request,
        'daily_salary/daily_salary_list.html',
        {
            'daily_salaries': page_obj,
            'page_obj': page_obj,
            'selected_department': department,
        }
    )
