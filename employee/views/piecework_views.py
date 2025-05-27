from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator
import json
from decimal import Decimal

from employee.models import Employee
from employee.models import Piecework
from employee.models import Work
from employee.forms import PieceworkForm, UpdatePieceworkForm
from employee.views.delete_attention import send_delete_warning


def create_piecework(request):
    """View to create a new piecework record."""
    errors = []
    department = request.GET.get('department', '')  # Default

    if request.method == 'POST':
        selected_works = request.POST.getlist('work_selected')
        amounts = {}
        for work_id in selected_works:
            amount = request.POST.get(f'amount_{work_id}')
            amounts[work_id] = amount

        form = PieceworkForm(request.POST, department=department)
        form.fields['employee'].queryset = Employee.objects.filter(department=department)
        form.fields['work'].queryset = Work.objects.filter(department=department)

        employee_ids = request.POST.getlist('employee')
        work_date = request.POST.get('work_date')
        type_work = request.POST.get('type_work')

        # Validation
        if not employee_ids:
            errors.append("At least one employee is required.")
        if not work_date:
            errors.append("Work date is required.")
        if not selected_works:
            errors.append("At least one work must be selected.")
        for work_id in selected_works:
            if not amounts[work_id]:
                errors.append(f"Amount for work {work_id} is required.")

        if not errors:
            employees = Employee.objects.filter(pk__in=employee_ids)
            # Calculate total money per hour for employees
            employees_money_sum = sum(emp.money_per_hour for emp in employees)

            # Calculate percentage for each employee
            employee_percentages = {}
            if employees_money_sum > 0:
                for emp in employees:
                    employee_percentages[emp.pk] = round((emp.money_per_hour / employees_money_sum) * 100, 2)
            else:
                for emp in employees:
                    employee_percentages[emp.pk] = 0
            
            # Calculate value from work.price for each employee using percentages
            employee_work_prices = {}  # {employee_id: {work_id: value}}
            for employee in employees:
                employee_work_prices[employee.pk] = {}
                for work_id in selected_works:
                    work = get_object_or_404(Work, pk=work_id)
                    try:
                        amount_decimal = Decimal(amounts[work_id])
                    except Exception:
                        errors.append(f"Invalid amount for work {work_id}.")
                        continue

                    # Calculate the value based on the employee's percentage
                    percent = employee_percentages[employee.pk]
                    value = round((work.price * percent) / 100, 2)
                    amount_price = round(value * amount_decimal, 2)
                    employee_work_prices[employee.pk][work_id] = value,

                    Piecework.objects.create(
                        employee=employee,
                        work=work,
                        amount=amount_decimal,
                        amount_price=amount_price,
                        work_date=work_date,
                        type_work=type_work
                    )

            if not errors:
                return redirect(
                    f"{reverse('piecework_list')}?department={department}"
                )
    else:
        form = PieceworkForm(department=department)
        form.fields['employee'].queryset = Employee.objects.filter(department=department)
        form.fields['work'].queryset = Work.objects.filter(department=department)

    existing_pieceworks = list(
        Piecework.objects.values(
            'employee_id', 'work_id', 'type_work', 'work_date'
        )
    )

    return render(
        request,
        'piecework/create_piecework.html',
        {
            'form': form,
            'object_type': 'Piecework',
            'cancel_url': f"{reverse('piecework_list')}?department={department}",
            'existing_pieceworks_json': json.dumps(existing_pieceworks, cls=DjangoJSONEncoder),
            'selected_department': department,
            'errors': errors,
        }
    )


def piecework_list(request):
    """View to list all piecework records with filtering and pagination."""
    department = request.GET.get('department', '')  # Default
    departments = Employee.objects.values_list('department', flat=True).distinct()
    
    # Only show pieceworks for employees in the selected department
    pieceworks = Piecework.objects.filter(employee__department=department)

    # Filtering
    employee_id = request.GET.get('employee_id')
    employee_name = request.GET.get('employee_name')
    work = request.GET.get('work')
    type_work = request.GET.get('type_work')
    type_material = request.GET.get('type_material')
    work_date = request.GET.get('work_date')
    record_date = request.GET.get('record_date')

    if employee_id:
        pieceworks = pieceworks.filter(employee__employee_id=employee_id)
    if employee_name:
        pieceworks = pieceworks.filter(employee__name__icontains=employee_name)
    if work:
        pieceworks = pieceworks.filter(work__pk=work)
    if type_work:
        pieceworks = pieceworks.filter(type_work=type_work)
    if type_material:
        pieceworks = pieceworks.filter(work__type_material=type_material)
    if work_date:
        pieceworks = pieceworks.filter(work_date=work_date)
    if record_date:
        pieceworks = pieceworks.filter(record_date__date=record_date)

    # For work dropdown
    works = Piecework.objects.values_list('work', flat=True).distinct()
    works = Work.objects.filter(pk__in=works)
    type_works = Piecework.objects.values_list('type_work', flat=True).distinct()
    type_materials = Piecework.objects.values_list('work__type_material', flat=True).distinct()

    # Sorting
    order_by = request.GET.get('order_by')
    direction = request.GET.get('direction')

    if order_by in ['work_date', 'record_date']:
        if direction == 'desc':
            pieceworks = pieceworks.order_by(f'-{order_by}')
        else:
            pieceworks = pieceworks.order_by(order_by)

    # Paginate the queryset
    paginator = Paginator(pieceworks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'piecework/piecework_list.html',
        {
            'pieceworks': page_obj,
            'page_obj': page_obj,
            'works': works,
            'type_works': type_works,
            'type_materials': type_materials,
            'departments': departments,
            'selected_department': department,
        }
    )


def update_piecework(request, pk):
    """View to update an existing piecework record."""
    piecework = get_object_or_404(Piecework, record_id=pk)
    department = request.GET.get('department', '')
    if request.method == 'POST':
        form = UpdatePieceworkForm(request.POST, instance=piecework, department=department)
        if form.is_valid():
            form.save()
            return redirect(
                f"{reverse('piecework_list')}?department={department}"
            )
    else:
        form = UpdatePieceworkForm(instance=piecework, department=department)
    return render(
        request,
        'piecework/update_piecework.html',
        {
        'form': form,
        'object_type': 'Piecework',
        'object_name': (
                f"Employee: {piecework.employee.employee_id} {piecework.employee.name}, "
                f"Work: {piecework.work.work_name}, "
                f"Type Work: {piecework.type_work}, Work Date: {piecework.work_date}"
            ),
        'cancel_url': f"{reverse('piecework_list')}?department={department}",
        }
    )


def delete_piecework(request, pk):
    """View to delete an existing piecework record."""
    piecework = get_object_or_404(Piecework, record_id=pk)
    department = request.GET.get('department', '')  # Default
    if request.method == 'POST':
        object_name = (
            f"Employee: {piecework.employee.employee_id} {piecework.employee.name}, "
            f"Work: {piecework.work.work_name}, Type Work: {piecework.type_work}, "
            f"Work Date: {piecework.work_date}"
        )
        piecework.delete()
        send_delete_warning(request, object_name)
        return redirect(f"{reverse('piecework_list')}?department={department}")
