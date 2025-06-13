from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.utils import timezone

from employee.models import Employee
from employee.models import DailySalary
from employee.forms import DailySalaryForm, UpdateDailySalaryForm
from employee.utils.delete_attention import send_delete_warning


def daily_salary_create(request):
    """View to create daily salary records for multiple employees, filtered by department."""
    department = request.GET.get('department') or request.session.get('department')

    # Filter employees by selected department, or show none if not selected
    employees = Employee.objects.none()
    if department:
        employees = Employee.objects.filter(department=department)

    # Ensure consistent ordering for pagination
    employees = employees.order_by('employee_id')

    errors = []

    if request.method == 'POST':
        selected_ids = request.POST.getlist('employee_ids')
        salary_date = request.POST.get('salary_date')
        hours_per_day = request.POST.get('hours_per_day')

        if not selected_ids or not salary_date or not hours_per_day:
            errors.append("Please select employees, date, and hours!")
        else:
            for emp_id in selected_ids:
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
                    DailySalary.objects.create(
                        employee_id=emp_id,
                        salary_date=salary_date,
                        hours_per_day=hours_per_day,
                    )
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


def daily_salary_list(request):
    """View to list all daily salaries with filtering and pagination."""
    department = request.GET.get('department') or request.session.get('department')

    daily_salaries = DailySalary.objects.filter(employee__department=department)

    # Filtering
    employee_id = request.GET.get('employee_id')
    employee_name = request.GET.get('employee_name')
    salary_date = request.GET.get('salary_date')
    record_date = request.GET.get('record_date')

    years = DailySalary.objects.values_list('salary_date__year', flat=True).distinct()

    if employee_id:
        daily_salaries = daily_salaries.filter(employee__employee_id=employee_id)
    if employee_name:
        daily_salaries = daily_salaries.filter(employee__name__icontains=employee_name)
    if salary_date:
        daily_salaries = daily_salaries.filter(salary_date=salary_date)
    if record_date:
        daily_salaries = daily_salaries.filter(record_date__date=record_date)

    # Handle sorting
    order_by = request.GET.get('order_by')
    direction = request.GET.get('direction')

    if order_by in ['salary_date', 'record_date']:
        if direction == 'desc':
            daily_salaries = daily_salaries.order_by(f'-{order_by}')
        else:
            daily_salaries = daily_salaries.order_by(order_by)
    else:
        daily_salaries = daily_salaries.order_by('-record_date')

    paginator = Paginator(daily_salaries, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'daily_salary/daily_salary_list.html',
        {
            'daily_salaries': page_obj,
            'page_obj': page_obj,
            'years': years,
            'selected_department': department,
        }
    )


def daily_salary_update(request, pk):
    """View to update an existing daily salary record."""
    daily_salary = get_object_or_404(DailySalary, pk=pk)
    department = request.GET.get('department') or request.session.get('department')

    if request.method == 'POST':
        form = UpdateDailySalaryForm(request.POST, instance=daily_salary)
        if form.is_valid():
            form.save()
            return redirect(
                #f"{reverse('daily_salary_list')}?department={department}"
                'daily_salary_list'
                )
    else:
        form = UpdateDailySalaryForm(instance=daily_salary)

    return render(
        request,
        'daily_salary/daily_salary_update.html',
        {
            'form': form,
            'object_type': 'Daily Salary',
            'object_name': (
                f"Employee: {daily_salary.employee.employee_id}/"
                f"{daily_salary.employee.name}, "
                f"Date: {daily_salary.salary_date}"
            ),
            'selected_department': department,
            'cancel_url': reverse('daily_salary_list'),
        }
    )


def daily_salary_delete(request, pk):
    """View to delete an existing daily salary record."""
    daily_salary = get_object_or_404(DailySalary, pk=pk)

    if request.method == 'POST':
        object_name = (
            f"Employee: {daily_salary.employee.employee_id}/"
            f"{daily_salary.employee.name}, "
            f"Date: {daily_salary.salary_date}"
        )
        daily_salary.delete()
        send_delete_warning(request, object_name)

        return redirect('daily_salary_list')
