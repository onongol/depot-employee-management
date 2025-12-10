from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.translation import gettext_lazy as _

from employee.utils.permissions import is_creater
from employee.mixins.success_messages_mixins import send_daily_salary_creation_message
from .context_builders import build_daily_salary_context
from .daily_salary_service import create_daily_salary_records


@login_required(login_url='login')
@user_passes_test(is_creater, login_url='login')
def daily_salary_create(request):
    """View to create daily salary records for multiple employees, filtered by department."""
    # Build context for the template
    context = build_daily_salary_context(request)

    # PRE-CHECK: no employees available for selected department
    if not context.get('employees'):
        return render(request, 'daily_salary/daily_salary_create.html', context)

    # Handle form submission
    if request.method == 'POST':
        selected_ids = [int(emp_id) for emp_id in request.POST.getlist('employee_ids')] # Convert to integers
        salary_date = request.POST.get('salary_date')
        hours_per_day = request.POST.get('hours_per_day')

        # Create daily salary records and handle errors
        result, errors = create_daily_salary_records(selected_ids, salary_date, hours_per_day)

        if errors:
            context['errors'] = errors
            return render(request, 'daily_salary/daily_salary_create.html', context)

        # Send success message and redirect to daily salary list
        send_daily_salary_creation_message(
            request,
            employees_dict=result['employees_dict'],
            selected_ids=selected_ids,
            salary_date=salary_date,
        )

        # Redirect to daily salary list with department filter
        department = context.get('selected_department')
        
        return redirect(f"{reverse('daily_salary_list')}?department={department}")

    return render(request, 'daily_salary/daily_salary_create.html', context)
