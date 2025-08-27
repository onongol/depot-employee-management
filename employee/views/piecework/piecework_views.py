import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from django.views.generic import UpdateView, DeleteView
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test

from employee.mixins.context_mixins import PieceworkContextMixin
from employee.mixins.delete_warning_mixins import DeleteWarningMixin
from employee.models import Employee
from employee.models import Piecework
from employee.models import Work
from employee.models import DailySalary
from employee.forms import PieceworkForm, UpdatePieceworkForm
from employee.utils.select_department import get_selected_department
from employee.utils.filters import filter_pieceworks
from employee.utils.pagination import paginate_queryset
from employee.views.piecework.piecework_calculation import piecework_calculate_records, piecework_calculate_update
from employee.utils.permissions import is_admin, OnlyAdminMixin, is_creater, OnlyCreaterMixin


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

        # Get the daily salary for the employee on the work date
        daily_salary = DailySalary.objects.filter(employee=employee, salary_date=work_date).first()
        # Get all daily salaries for the department on the work date
        employees_salary = DailySalary.objects.filter(employee__department=department, salary_date=work_date)

        # Calculate amount_price using business logic function
        amount_price = piecework_calculate_update(work, amount, daily_salary, employees_salary)
        piecework.amount_price = amount_price

        form.save()

        return redirect('piecework_list')


class PieceworkDeleteView(LoginRequiredMixin, OnlyAdminMixin,PieceworkContextMixin, DeleteWarningMixin, DeleteView):
    login_url = 'login'
    template_name = "piecework/piecework_delete.html"

    # Handle the deletion and send a warning.
    def get_redirect_url(self):
        return self.success_url
    
    def get_object_name(self):
        return (
            f"{self.object.employee.employee_id}/{self.object.employee.name}/{self.object.work.work_name}/{self.object.type_work}/{self.object.work_date}"
        )


@user_passes_test(is_creater, login_url='login')
@login_required(login_url='login')
def piecework_create(request):
    """View to create piecework records for multiple employees and works."""
    department = get_selected_department(request)
    employees = (
        Employee.objects.filter(department=department, is_active=True).order_by('employee_id')
        if department else Employee.objects.none()
    )
    works = (
        Work.objects.filter(department=department).order_by('work_name')
        if department else Work.objects.none()
    )
    today = timezone.now().date()
    errors = []

    if request.method == 'POST':
        work_date = request.POST.get('work_date')
        type_work = request.POST.get('type_work')
        wagon_number = (request.POST.get('wagon_number'))
        selected_employee_ids = request.POST.getlist('employee_ids')
        selected_work_ids = request.POST.getlist('work_ids')
        amounts = {wid: request.POST.get(f'amount_{wid}') for wid in selected_work_ids}

        # Validate required fields
        if not selected_employee_ids:
            errors.append("Please select at least one employee.")
        if not selected_work_ids:
            errors.append("Please select at least one work.")

        # Prefetch all selected works in a single query for efficient access
        works_dict = {str(work.pk): work for work in Work.objects.filter(pk__in=selected_work_ids)}

        # Check for missing amounts for any selected work
        missing_amounts = [
            wid for wid in selected_work_ids if not amounts.get(wid)
        ]    

        if not work_date or not type_work:
            errors.append("Please select work date, type work.")    
        elif missing_amounts:
            # If there are missing amounts, get the work names for error reporting
            missing_work_names = [
                works_dict[wid].work_name for wid in missing_amounts if wid in works_dict
            ]
            errors.append(f"Please fill in the amount for all selected work(s): {', '.join(missing_work_names)}.")
        else:
            # --- NEW DAILY SALARY CHECK LOGIC ---
            # Get all DailySalary records for selected employees and date
            employees_salary = DailySalary.objects.filter(
                employee__employee_id__in=selected_employee_ids,
                salary_date=work_date,
            )
            # Find employees without a DailySalary for the date
            employees_with_salary_ids = set(str(ds.employee.employee_id) for ds in employees_salary)
            missing_salary_employees = [
                emp for emp in Employee.objects.filter(employee_id__in=selected_employee_ids)
                if str(emp.employee_id) not in employees_with_salary_ids
            ]
            if missing_salary_employees:
                missing_names = [f"{emp.employee_id}/{emp.name}" for emp in missing_salary_employees]
                errors.append(
                    f"First create Daily Salary for these employee(s): {', '.join(missing_names)} for the selected date {work_date}."
                )
            else:
                # --- Business logic: Calculate amount_price for each employee and work ---
                # This function returns a list of dicts with calculated data and a list of errors                
                results, calc_errors = piecework_calculate_records(
                    employees_salary=employees_salary,
                    selected_work_ids=selected_work_ids,
                    amounts=amounts,
                    works_dict=works_dict,
                    work_date=work_date,
                    type_work=type_work,
                    wagon_number=wagon_number,
                )
                errors.extend(calc_errors)
                if not errors:
                    try:
                        # Use atomic transaction to ensure all records are created together
                        with transaction.atomic():
                            for data in results:
                                Piecework.objects.create(**data)
                    except Exception as e:
                        errors.append(f"Error creating piecework records: {str(e)}")
            if not errors:
                return redirect(f"{reverse('piecework_list')}?department={department}")
                
    # Get existing pieceworks for the department for use in the frontend (e.g., to prevent duplicates)
    existing_pieceworks = list(
        Piecework.objects.filter(employee__department=department)
        .values(
            'employee_id', 'work_id', 'type_work', 'work_date'
        )
    )

    # Render the template with all context data
    return render(
        request,
        'piecework/piecework_create.html',
        {   
            'form': PieceworkForm(department=department),
            'object_type': 'Piecework',
            'employees': employees,
            'works': works,
            'today': today,
            'errors': errors,
            'selected_department': department,
            'cancel_url': reverse('piecework_list'),
            'existing_pieceworks_json': json.dumps(existing_pieceworks, cls=DjangoJSONEncoder), # Serialize existing pieceworks for frontend validation
        }
    )


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

    # Prepare dropdown data for type_work and type_material filters
    type_works = (
        Piecework.objects.filter(work__department=department)
        .values_list('type_work', flat=True)
        .distinct()
    )
    type_materials = (
        Piecework.objects.filter(work__department=department)
        .values_list('work__type_material', flat=True)
        .distinct()
    )

    # Extract filter parameters from the request
    employee_id = request.GET.get('employee_id')
    employee_name = request.GET.get('employee_name')
    work = request.GET.get('work')
    type_work = request.GET.get('type_work')
    type_material = request.GET.get('type_material')
    work_date = request.GET.get('work_date')
    record_date = request.GET.get('record_date')

    # Apply all filters using a reusable filter function
    pieceworks = filter_pieceworks(
        pieceworks,
        employee_id=employee_id,
        employee_name=employee_name,
        work=work,
        type_work=type_work,
        type_material=type_material,
        work_date=work_date,
        record_date=record_date
    )

    # Sorting logic: allows sorting by work_date or record_date, default is by record_date descending
    order_by = request.GET.get('order_by')
    direction = request.GET.get('direction')

    if order_by in ['work_date', 'record_date']:
        if direction == 'desc':
            pieceworks = pieceworks.order_by(f'-{order_by}')
        else:
            pieceworks = pieceworks.order_by(order_by)
    else:
        pieceworks = pieceworks.order_by('-record_date')

    # Paginate the results, 10 records per page
    page_obj = paginate_queryset(request, pieceworks)

    # Render the template with all context data
    return render(
        request,
        'piecework/piecework_list.html',
        {
            'pieceworks': page_obj,
            'page_obj': page_obj,
            'type_works': type_works,
            'type_materials': type_materials,
            'selected_department': department,
        }
    )
