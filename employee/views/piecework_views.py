from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator
import json
from decimal import Decimal
from django.utils import timezone

from employee.models import Employee
from employee.models import Piecework
from employee.models import Work
from employee.models import DailySalary
from employee.forms import PieceworkForm, UpdatePieceworkForm
from employee.views.delete_attention import send_delete_warning


def create_piecework(request):
    """View to create piecework records for multiple employees and works."""
    department = request.GET.get('department') or request.session.get('department')
    
    employees = (
        Employee.objects.filter(department=department) if department else Employee.objects.none()
        )
    works = (
        Work.objects.filter(department=department) if department else Work.objects.none()
    )
    
    # Ensure consistent ordering for pagination
    employees = employees.order_by('employee_id')
    works = works.order_by('work_name')
    
    errors = []
    today = timezone.now().date()

    work_paginator = Paginator(works, 10)
    work_page_number = request.GET.get('work_page')
    work_page_obj = work_paginator.get_page(work_page_number)

    if request.method == 'POST':
        work_date = request.POST.get('work_date')
        type_work = request.POST.get('type_work')
        selected_employee_ids = request.POST.getlist('employee_ids')
        selected_work_ids = request.POST.getlist('work_ids')
        amounts = {wid: request.POST.get(f'amount_{wid}') for wid in selected_work_ids}
    
        if not work_date or not type_work or not selected_employee_ids or not selected_work_ids:
            errors.append("Please select work date, type work, employees, and works.")
        else:
            # Get DailySalary records for selected employees and date
            employees_salary = DailySalary.objects.filter(
                employee__employee_id__in=selected_employee_ids,
                salary_date=work_date,
            )
            if not employees_salary.exists():
                errors.append(
                    f"First create Daily Salary of these employee(s) {selected_employee_ids} for the selected date {work_date}."
                )
            else:
                # Calculate employee sum salary for the given date
                employees_money_sum = sum(emp.salary_day for emp in employees_salary)
                # Calculate percentages for each employee
                employee_percentages = {}
                if employees_money_sum > 0:
                    for emp in employees_salary:
                        employee_percentages[emp.employee.employee_id] = round((emp.salary_day / employees_money_sum) * 100, 2)
                else:
                    for emp in employees_salary:
                        employee_percentages[emp.employee.employee_id] = 0
                # Create Piecework records for each employee and work
                for emp in employees_salary:
                    emp_id = emp.employee.employee_id
                    percent = employee_percentages[emp_id]
                    for work_id in selected_work_ids:
                        amount = amounts.get(work_id)
                        if not amount:
                            errors.append(f"Amount required for work {work_id}.")
                            continue
                        try:
                            amount_decimal = Decimal(amount)
                        except Exception:
                            errors.append(f"Invalid amount for work {work_id}.")
                            continue

                        # Validate amount
                        work = Work.objects.get(pk=work_id)
                        # Calculate amount_price
                        value = round((work.price * percent) / 100, 2)
                        amount_price = round(value * amount_decimal, 2)
                        # Create Piecework record
                        Piecework.objects.create(
                            employee_id=emp_id,
                            work_id=work_id,
                            amount=amount_decimal,
                            amount_price=amount_price,
                            work_date=work_date,
                            type_work=type_work,    
                        )
            if not errors:
                return redirect(f"{reverse('piecework_list')}?department={department}")
                
    # Get existing pieceworks for the department  
    existing_pieceworks = list(
        Piecework.objects.values(
            'employee_id', 'work_id', 'type_work', 'work_date'
        )
    )
            
    return render(
        request,
        'piecework/create_piecework.html',
        {   
            'form': PieceworkForm(department=department),
            'object_type': 'Piecework',
            'employees': employees,
            'work_page_obj': work_page_obj,
            'today': today,
            'errors': errors,
            'selected_department': department,
            'cancel_url': reverse('piecework_list'),
            'existing_pieceworks_json': json.dumps(existing_pieceworks, cls=DjangoJSONEncoder),
        }
    )


def piecework_list(request):
    """View to list all piecework records with filtering and pagination."""
    department = request.GET.get('department') or request.session.get('department')
    
    # Only show pieceworks for employees in the selected department
    pieceworks = Piecework.objects.filter(employee__department=department)

    # For work dropdown
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
        pieceworks = pieceworks.filter(work__work_name=work)
    if type_work:
        pieceworks = pieceworks.filter(type_work=type_work)
    if type_material:
        pieceworks = pieceworks.filter(work__type_material=type_material)
    if work_date:
        pieceworks = pieceworks.filter(work_date=work_date)
    if record_date:
        pieceworks = pieceworks.filter(record_date__date=record_date)

    # Sorting
    order_by = request.GET.get('order_by')
    direction = request.GET.get('direction')

    if order_by in ['work_date', 'record_date']:
        if direction == 'desc':
            pieceworks = pieceworks.order_by(f'-{order_by}')
        else:
            pieceworks = pieceworks.order_by(order_by)
    else:
        pieceworks = pieceworks.order_by('-record_date')

    paginator = Paginator(pieceworks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

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


def update_piecework(request, pk):
    """View to update an existing piecework record."""
    piecework = get_object_or_404(Piecework, record_id=pk)
    department = request.GET.get('department') or request.session.get('department')

    if request.method == 'POST':
        form = UpdatePieceworkForm(request.POST, instance=piecework, department=department)
        if form.is_valid():
            # Calculate amount_price before saving
            amount = form.cleaned_data.get('amount')
            work = piecework.work
            work_date = piecework.work_date
            #type_work = piecework.type_work
            employee = piecework.employee

            # Get DailySalary for this employee and date
            daily_salary = (
                DailySalary.objects.filter(employee=employee, salary_date=work_date)
                .first()
            )
            # Get all DailySalary for this date and department
            employees_salary = DailySalary.objects.filter(
                employee__department=department,
                salary_date=work_date,
            )
            # Calculate employees_money_sum
            employees_money_sum = sum(emp.salary_day for emp in employees_salary)
            # Calculate percent
            percent = 0
            if employees_money_sum > 0 and daily_salary:
                percent = round((daily_salary.salary_day / employees_money_sum) * 100, 2)
            # Calculate amount_price
            value = round((work.price * percent) / 100, 2)
            amount_price = round(value * amount, 2) if amount is not None else 0

            piecework.amount_price = amount_price

            form.save()

            return redirect(
                #f"{reverse('piecework_list')}?department={department}"
                'piecework_list'
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
            'selected_department': department,
            'cancel_url': reverse('piecework_list'),
        }
    )


def delete_piecework(request, pk):
    """View to delete an existing piecework record."""
    piecework = get_object_or_404(Piecework, record_id=pk)

    if request.method == 'POST':
        object_name = (
            f"Employee: {piecework.employee.employee_id} {piecework.employee.name}, "
            f"Work: {piecework.work.work_name}, Type Work: {piecework.type_work}, "
            f"Work Date: {piecework.work_date}"
        )
        piecework.delete()
        send_delete_warning(request, object_name)

        return redirect('piecework_list')
