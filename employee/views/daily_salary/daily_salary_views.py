import logging
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import UpdateView, DeleteView
from django.db import transaction
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _

from employee.mixins.context_mixins import DailySalaryContextMixin
from employee.mixins.delete_mixins import DeleteProtectionMixin
from employee.mixins.block_message_mixins import BlockMessageMixin
from employee.models import Employee
from employee.models import DailySalary
from employee.models import Piecework
from employee.forms import DailySalaryForm, UpdateDailySalaryForm
from employee.utils.select_department import get_selected_department
from employee.utils.filters import filter_daily_salaries
from employee.utils.pagination import paginate_queryset
from employee.utils.converting_date import format_date
from employee.utils.permissions import OnlyAdminMixin, is_creater
from employee.utils.sorting import apply_ordering
from employee.utils.selects import get_distinct_values
from employee.mixins.success_messages_mixins import send_daily_salary_creation_message


class DailySalaryUpdateView(LoginRequiredMixin, OnlyAdminMixin, DailySalaryContextMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    form_class = UpdateDailySalaryForm
    template_name = "daily_salary/daily_salary_update.html"
    success_message = _("Daily Salary updated successfully.")


class DailySalaryDeleteView(LoginRequiredMixin, OnlyAdminMixin, DailySalaryContextMixin, BlockMessageMixin, DeleteProtectionMixin, DeleteView):
    login_url = 'login'
    template_name = "daily_salary/daily_salary_confirm_delete.html"
    block_related_models = [_('Daily Salary'), _('Piecework')]

    # Get related piecework records to check if deletion is allowed.
    def get_related_objects(self):
        return Piecework.objects.filter(
            employee=self.object.employee,
            work_date=self.object.salary_date
        )
        
    # Handle the deletion and send a warning.
    def get_redirect_url(self):
        return self.success_url
    
    def get_object_name(self):
        return (
            f"{self.object.employee.employee_id}/{self.object.employee.name}/{self.object.salary_date}"
        )


@login_required(login_url='login')
@user_passes_test(is_creater, login_url='login')
def daily_salary_create(request):
    """View to create daily salary records for multiple employees, filtered by department."""
    department = get_selected_department(request)

    # Filter employees by selected department, or show none if not selected
    employees = Employee.objects.none()
    if department:
        employees = Employee.objects.filter(department=department, is_active=True)  # Only active employees

    # Get distinct job titles for filtering dropdown
    job_titles = get_distinct_values(Employee, 'job_title', department, department_field='department')

    # Ensure consistent ordering for pagination or display
    employees = employees.order_by('employee_id')
    
    errors = []

    if request.method == 'POST':
        selected_ids = request.POST.getlist('employee_ids')
        selected_ids = [int(emp_id) for emp_id in selected_ids] # Convert selected_ids to integers
        salary_date = request.POST.get('salary_date')
        hours_per_day = request.POST.get('hours_per_day')

        # Check if any employees are selected
        if not selected_ids:
            errors.append(_("Please select at least one employee."))

        # Validate required fields
        if not salary_date or not hours_per_day:
            errors.append(_("Please select date and hours!"))

        # Validate required fields
        if not errors:
            try:
                # Use atomic transaction to ensure all records are created together
                with transaction.atomic():
                    existing_records = set(DailySalary.objects.filter(
                        employee_id__in=selected_ids,
                        salary_date=salary_date
                    ).values_list('employee_id', flat=True))

                    # Map employee IDs to their Employee objects
                    employees_dict = {e.employee_id: e for e in Employee.objects.filter(employee_id__in=selected_ids)}

                    # Check for duplicates and create records
                    new_records = []
                    for emp_id in selected_ids:
                        if emp_id in existing_records:
                            emp = employees_dict.get(emp_id)
                            errors.append(
                                _("Daily salary record for Employee: %(employee)s on %(date)s already exists!") % {
                                    'employee': f"{emp_id}/{emp.name}",
                                    'date': salary_date
                                }
                            )
                        else:
                            emp = employees_dict.get(emp_id)

                            # Calculate salary_day manually
                            salary_day = float(hours_per_day) * float(emp.money_per_hour)

                            # Create new DailySalary instance
                            new_records.append(
                                DailySalary(
                                    employee_id=emp_id,
                                    salary_date=salary_date,
                                    hours_per_day=hours_per_day,
                                    salary_day=salary_day
                                )
                            )
                    if new_records and not errors:
                        # Bulk create new records DailySalary
                        try:
                            DailySalary.objects.bulk_create(new_records)

                            # Success message
                            send_daily_salary_creation_message(
                                request,
                                employees_dict=employees_dict,
                                selected_ids=selected_ids,
                                salary_date=salary_date,
                            )
                        except Exception as exc:
                            logging.exception("Bulk create DailySalary failed")
                            errors.append(_("Error saving daily salary records."))
            except Exception as e:
                errors.append(_("Error creating daily salary records: %(error)s") % {'error': str(e)})
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
            'job_titles': job_titles,
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

    # Reduce DB queries in template
    daily_salaries = daily_salaries.select_related('employee')

    # Get distinct job titles for filtering dropdown
    job_titles = get_distinct_values(Employee, 'job_title', department, department_field='department')

    # Filtering by employee ID, name, salary date, and record date
    employee_id = request.GET.get('employee_id')
    employee_name = request.GET.get('employee_name')
    job_title = request.GET.get('job_title')
    salary_date = format_date(request.GET.get('salary_date'))
    record_date = format_date(request.GET.get('record_date'))

    # Apply filters to the daily salaries queryset using reusable filter functions
    daily_salaries = filter_daily_salaries(
        daily_salaries, 
        employee_id=employee_id, 
        employee_name=employee_name, 
        job_title=job_title,
        salary_date=salary_date, 
        record_date=record_date
    )

    # Sorting
    order_by = request.GET.get('order_by')
    direction = request.GET.get('direction')
    
    daily_salaries = apply_ordering(
        daily_salaries, order_by, direction, allowed_fields=['salary_date', 'record_date'], default='-salary_date'
    )

    # Paginate the results, 10 records per page
    page_obj = paginate_queryset(request, daily_salaries)

    # Preserve filter values in the context for template rendering
    filters = {
        'employee_id': employee_id or '',
        'employee_name': employee_name or '',
        'job_title': job_title or '',
        'salary_date': salary_date or '',
        'record_date': record_date or '',
    }

    return render(
        request,
        'daily_salary/daily_salary_list.html',
        {
            'daily_salaries': page_obj,
            'page_obj': page_obj,
            'selected_department': department,
            'job_titles': job_titles,
            'filters': filters,
        }
    )
