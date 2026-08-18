from dataclasses import asdict

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.urls import reverse

from employee.views.daily_salary.daily_salary_create.daily_salary_create_prepare import (
    prepare_daily_salary_create,
)
from employee.views.daily_salary.daily_salary_create.daily_salary_create_service import (
    create_daily_salary_records,
)
from employee.views.daily_salary.daily_salary_create.daily_salary_messages import (
    send_daily_salary_creation_message,
)


@login_required
@permission_required("employee.add_dailysalary")
def daily_salary_create(request):
    """View to create daily salary records for multiple employees, filtered by department."""
    # Build context for the template
    dsc_context = prepare_daily_salary_create(request)

    # PRE-CHECK: no employees available for selected department
    if not dsc_context.employees:
        return render(
            request, "daily_salary/daily_salary_create.html", asdict(dsc_context)
        )

    # Handle form submission
    if request.method == "POST":
        selected_ids = [int(emp_id) for emp_id in request.POST.getlist("employee_ids")]
        salary_date = request.POST.get("salary_date")
        hours_per_day = request.POST.get("hours_per_day")

        employees_dict, errors = create_daily_salary_records(
            selected_ids, salary_date, hours_per_day, user=request.user
        )

        if errors:
            dsc_context.errors = errors
            return render(
                request, "daily_salary/daily_salary_create.html", asdict(dsc_context)
            )

        send_daily_salary_creation_message(
            request,
            employees_dict=employees_dict,
            selected_ids=selected_ids,
            salary_date=salary_date,
        )

        # Redirect to daily salary list with department filter
        department = dsc_context.selected_department
        return redirect(f"{reverse('daily_salary_list')}?department={department}")

    return render(request, "daily_salary/daily_salary_create.html", asdict(dsc_context))
