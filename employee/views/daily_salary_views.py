from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator

from employee.models import DailySalary
from employee.forms import DailySalaryForm, UpdateDailySalaryForm
from employee.views.delete_attention import send_delete_warning


def create_daily_salary(request):
    """View to create a new daily salary record."""
    if request.method == 'POST':
        form = DailySalaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('daily_salary_list')
    else:
        form = DailySalaryForm()
    return render(
        request,
        'daily_salary/create_daily_salary.html',
        {
            'form': form,
            'object_type': 'Daily Salary',
            'cancel_url': reverse('daily_salary_list'),
        }
    )


def daily_salary_list(request):
    """View to list all daily salaries with filtering and pagination."""
    daily_salaries = DailySalary.objects.all()

    # Filtering
    employee_id = request.GET.get('employee_id')
    employee_name = request.GET.get('employee_name')
    department = request.GET.get('department')
    salary_date = request.GET.get('salary_date')
    record_date = request.GET.get('record_date')

    years = (
        DailySalary.objects.values_list('salary_date__year', flat=True)
        .distinct()
    )

    # Get all unique departments from Employee table
    departments = (
        DailySalary.objects.values_list('employee__department', flat=True)
        .distinct()
    )

    if employee_id:
        daily_salaries = daily_salaries.filter(employee__employee_id=employee_id)
    if employee_name:
        daily_salaries = daily_salaries.filter(employee__name__icontains=employee_name)
    if department:
        daily_salaries = daily_salaries.filter(employee__department=department)
    if salary_date:
        daily_salaries = daily_salaries.filter(salary_date=salary_date)
    if record_date:
        daily_salaries = daily_salaries.filter(record_date=record_date)

    # Handle sorting
    order_by = request.GET.get('order_by')
    direction = request.GET.get('direction')
    
    if order_by in ['salary_date', 'record_date']:
        if direction == 'desc':
            daily_salaries = daily_salaries.order_by(f'-{order_by}')
        else:
            daily_salaries = daily_salaries.order_by(order_by)

    # Paginate the queryset
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
            'departments': departments,
        }
    )


def update_daily_salary(request, pk):
    """View to update an existing daily salary record."""
    daily_salary = get_object_or_404(DailySalary, pk=pk)
    if request.method == 'POST':
        form = UpdateDailySalaryForm(request.POST, instance=daily_salary)
        if form.is_valid():
            form.save()
            return redirect('daily_salary_list')
    else:
        form = UpdateDailySalaryForm(instance=daily_salary)
    return render(
        request,
        'daily_salary/update_daily_salary.html',
        {
            'form': form,
            'object_type': 'Daily Salary',
            'object_name': (
                f"Employee: {daily_salary.employee.employee_id} "
                f"{daily_salary.employee.name}, "
                f"Date: {daily_salary.salary_date}"
            ),
            'cancel_url': reverse('daily_salary_list'),
        }
    )


def delete_daily_salary(request, pk):
    """View to delete an existing daily salary record."""
    daily_salary = get_object_or_404(DailySalary, pk=pk)
    if request.method == 'POST':
        object_name = (
            f"Employee: {daily_salary.employee.employee_id} "
            f"{daily_salary.employee.name}, "
            f"Date: {daily_salary.salary_date}"
        )
        daily_salary.delete()
        send_delete_warning(request, object_name)
        return redirect('daily_salary_list')
