from django.shortcuts import render, redirect
from django.db.models import Sum
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _

from employee.mixins.context_mixins import PieceworkContextMixin
from employee.mixins.delete_mixins import DeleteWarningMixin
from employee.models import Piecework
from employee.models import DailySalary
from employee.forms import UpdatePieceworkForm
from employee.utils.select_department import get_selected_department
from employee.utils.filters import filter_pieceworks
from employee.utils.pagination import paginate_queryset
from employee.utils.sorting import apply_ordering
from employee.utils.selects import get_distinct_values
from employee.utils.select_type_wagon import get_type_wagon_filter_values
from employee.utils.permissions import OnlyAdminMixin, is_creater
from employee.views.piecework.piecework_calculation import piecework_calculate_update
from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS


class PieceworkUpdateView(LoginRequiredMixin, OnlyAdminMixin, PieceworkContextMixin, UpdateView):
    login_url = 'login'
    form_class = UpdatePieceworkForm
    template_name = 'piecework/piecework_update.html'

    def get_form_kwargs(self):
        """Add department to form kwargs for filtering."""
        kwargs = super().get_form_kwargs()
        department = get_selected_department(self.request)
        kwargs['department'] = department
        return kwargs

    def form_valid(self, form):
        """Handle form validation and calculate amount price based on daily salary."""
        piecework = form.instance
        amount = form.cleaned_data.get('amount')
        work = piecework.work
        work_date = piecework.work_date
        employee = piecework.employee
        department = get_selected_department(self.request)

        wagon_number = form.cleaned_data.get('wagon_number')
        if not wagon_number:
            piecework.wagon_number = None

        # Get the daily salary for the employee on the work date
        daily_salary = DailySalary.objects.filter(employee=employee, salary_date=work_date).first()

        # Get all daily salaries for the department on the work date
        employees_salary = DailySalary.objects.filter(employee__department=department, salary_date=work_date)

        # Calculate amount_price using business logic function
        amount_price = piecework_calculate_update(work, amount, daily_salary, employees_salary)

        piecework.amount_price = amount_price

        form.save()

        return redirect('piecework_list')


class PieceworkDeleteView(LoginRequiredMixin, OnlyAdminMixin, PieceworkContextMixin, DeleteWarningMixin, DeleteView):
    login_url = 'login'
    template_name = "piecework/piecework_delete.html"

    # Handle the deletion and send a warning.
    def get_redirect_url(self):
        return self.success_url
    
    def get_object_name(self):
        return (
            f"{self.object.employee.employee_id}/{self.object.employee.name}/{self.object.work.work_name}/{self.object.type_work}/{self.object.work_date}"
        )


@login_required(login_url='login')
@user_passes_test(is_creater, login_url='login')
def piecework_create(request):
    """View to create new piecework records."""
    # Circular import avoidance
    from employee.views.daily_work.daily_work_piecework_create import daily_work_piecework_create

    return daily_work_piecework_create(request)


@login_required(login_url='login')
def piecework_list(request):
    """View to list all piecework records with filtering and pagination."""
    # Only show pieceworks for employees in the selected department
    department = get_selected_department(request)

    # If not an employee, show all pieceworks in the department
    if request.user.groups.filter(name='Employees').exists():
        pieceworks = Piecework.objects.select_related('employee', 'work').filter(
            employee__user=request.user, employee__department=department, employee__is_active=True
        )
    else:
        # If not an employee, show all pieceworks in the department
        pieceworks = Piecework.objects.select_related('employee', 'work').filter(employee__department=department, employee__is_active=True)

    # Get distinct values for filtering dropdown
    job_titles = get_distinct_values(Piecework, 'job_title', department, department_field='employee__department')
    type_works = get_distinct_values(Piecework, 'type_work', department, department_field='work__department')
    type_materials = get_distinct_values(Piecework, 'work__type_material', department, department_field='work__department')

    # Get snapshot values of type_wagon from Piecework
    type_wagons = get_type_wagon_filter_values(department, source_model='piecework')

    # Extract filter parameters from the request
    employee_id = request.GET.get('employee_id')
    employee_name = request.GET.get('employee_name')
    job_title = request.GET.get('job_title')
    work_name = request.GET.get('work_name')
    type_work = request.GET.get('type_work')
    wagon_number = request.GET.get('wagon_number')
    type_wagon = request.GET.get('type_wagon')
    type_material = request.GET.get('type_material')
    range_date = request.GET.get('range_date')
    record_date = request.GET.get('record_date')

    # Apply all filters using a reusable filter function
    pieceworks = filter_pieceworks(
        pieceworks,
        employee_id=employee_id,
        employee_name=employee_name,
        job_title=job_title,
        work_name=work_name,
        type_work=type_work,
        wagon_number=wagon_number,
        type_wagon=type_wagon,
        type_material=type_material,
        range_date=range_date,
        record_date=record_date
    )

    # Aggregation for totals
    totals = pieceworks.aggregate(
        total_amount=Sum('amount'),
        total_time=Sum('amount_time'),
        total_price=Sum('amount_price')
    )

    # Sorting
    order_by = request.GET.get('order_by')
    direction = request.GET.get('direction')

    pieceworks = apply_ordering(
        pieceworks, order_by, direction, allowed_fields=['work_date', 'record_date'], default='-work_date'
    )

    # Paginate the results, 10 records per page
    page_obj = paginate_queryset(request, pieceworks)

    # Prepare current filter values for template context
    filters = {
        'employee_id': employee_id or '',
        'employee_name': employee_name or '',
        'job_title': job_title or '',
        'work_name': work_name or '',
        'type_work': type_work or '',
        'wagon_number': wagon_number or '',
        'type_wagon': type_wagon or '',
        'type_material': type_material or '',
        'range_date': range_date or '',
        'record_date': record_date or '',
    }

    # Render the template with all context data
    return render(
        request,
        'piecework/piecework_list.html',
        {   
            'employee_id': employee_id,
            'employee_name': employee_name,
            'job_title': job_title,
            'work_name': work_name,
            'type_work': type_work,
            'wagon_number': wagon_number,
            'type_wagon': type_wagon,
            'range_date': range_date,
            'record_date': record_date,
            'pieceworks': page_obj,
            'page_obj': page_obj,
            'selected_department': department,
            'type_works': type_works,
            'type_materials': type_materials,
            'job_titles': job_titles,
            'type_wagons': type_wagons,
            'ALLOWED_WAGON_DEPARTMENTS': ALLOWED_WAGON_DEPARTMENTS,
            'totals': totals,
            'filters': filters,
        }
    )
