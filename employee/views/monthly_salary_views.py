from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator

from employee.models import MonthlySalary
from employee.forms import MonthlySalaryForm, UpdateMonthlySalaryForm
from employee.views.delete_attention import send_delete_warning


def create_monthly_salary(request):
    """View to create a new monthly salary record."""
    if request.method == 'POST':
        form = MonthlySalaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('monthly_salary_list')
    else:
        form = MonthlySalaryForm()
    return render(
        request,
        'monthly_salary/create_monthly_salary.html',
        {
            'form': form,
            'object_type': 'Monthly Salary',
            'cancel_url': reverse('monthly_salary_list'),
        }
    )


def monthly_salary_list(request):
    """View to list all monthly salaries with filtering and pagination."""
    monthly_salaries = MonthlySalary.objects.all()

    # Filtering
    employee_id = request.GET.get('employee_id')
    employee_name = request.GET.get('employee_name')
    month = request.GET.get('month')
    year = request.GET.get('year')
    record_date = request.GET.get('record_date')

    # Constants for month choices
    MONTH_CHOICES = [
        (1, '01'), (2, '02'), (3, '03'), (4, '04'),
        (5, '05'), (6, '06'), (7, '07'), (8, '08'),
        (9, '09'), (10, '10'), (11, '11'), (12, '12'),
    ]

    years = (
        MonthlySalary.objects.values_list('year', flat=True)
        .distinct()
    )

    if employee_id:
        monthly_salaries = monthly_salaries.filter(employee__employee_id=employee_id)
    if employee_name:
        monthly_salaries = monthly_salaries.filter(employee__name__icontains=employee_name)
    if month:
        monthly_salaries = monthly_salaries.filter(month=month)
    if year:
        monthly_salaries = monthly_salaries.filter(year=year)
    if record_date:
        monthly_salaries = monthly_salaries.filter(record_date=record_date)

    # Handle sorting
    order_by = request.GET.get('order_by')
    direction = request.GET.get('direction')
    
    if order_by in ['month', 'year', 'record_date']:
        if direction == 'desc':
            monthly_salaries = monthly_salaries.order_by(f'-{order_by}')
        else:
            monthly_salaries = monthly_salaries.order_by(order_by)

    # Paginate the queryset
    paginator = Paginator(monthly_salaries, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'monthly_salary/monthly_salary_list.html',
        {
            'monthly_salaries': page_obj,
            'page_obj': page_obj,
            'months': MONTH_CHOICES,
            'years': years,
        }
    )


def update_monthly_salary(request, pk):
    """View to update an existing monthly salary record."""
    monthly_salary = get_object_or_404(MonthlySalary, pk=pk)
    if request.method == 'POST':
        form = UpdateMonthlySalaryForm(request.POST, instance=monthly_salary)
        if form.is_valid():
            form.save()
            return redirect('monthly_salary_list')
    else:
        form = UpdateMonthlySalaryForm(instance=monthly_salary)
    return render(
        request,
        'monthly_salary/update_monthly_salary.html',
        {
            'form': form,
            'object_type': 'Monthly Salary',
            'object_name': (
                f"Employee: {monthly_salary.employee.employee_id} "
                f"{monthly_salary.employee.name}, "
                f"Date: {monthly_salary.month}/{monthly_salary.year}"
            ),
            'cancel_url': reverse('monthly_salary_list'),
        }
    )


def delete_monthly_salary(request, pk):
    """View to delete an existing monthly salary record."""
    monthly_salary = get_object_or_404(MonthlySalary, pk=pk)
    if request.method == 'POST':
        object_name = (
            f"Employee: {monthly_salary.employee.employee_id} "
            f"{monthly_salary.employee.name}, "
            f"Date: {monthly_salary.month}/{monthly_salary.year}"
        )
        monthly_salary.delete()
        send_delete_warning(request, object_name)
        return redirect('monthly_salary_list')
