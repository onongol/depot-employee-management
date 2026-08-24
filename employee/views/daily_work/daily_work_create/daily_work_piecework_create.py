from dataclasses import asdict

from django.shortcuts import redirect, render
from django.urls import reverse

from employee.views.daily_work.daily_work_create.daily_work_create_prepare import (
    daily_work_piecework_create_prepare,
)
from employee.views.daily_work.daily_work_create.daily_work_create_service import (
    create_daily_work_piecework_records,
)
from employee.views.daily_work.daily_work_create.messages.create_success_message import (
    send_success_creation_message,
)
from employee.views.daily_work.daily_work_create.post_data.extract_post_data import (
    extract_post_data,
)


def daily_work_piecework_create(request):
    """Handle the creation of daily work and piecework entries."""
    context = daily_work_piecework_create_prepare(request)

    # PRE-CHECK: no employees available for selected date/department
    if not context.employees:
        return render(
            request, "daily_work/daily_work_piecework_create.html", asdict(context)
        )

    # Process form submission: extract data, create records, handle errors, show success message, and redirect to the daily work list
    if request.method == "POST":
        post_data = extract_post_data(request)
        results, works_dict, errors = create_daily_work_piecework_records(
            request_data=post_data,
            user=request.user,
        )

        if errors:
            context.errors = errors
            return render(
                request,
                "daily_work/daily_work_piecework_create.html",
                asdict(context),
            )

        send_success_creation_message(
            request,
            results=results,
            works_dict=works_dict,
            work_date=post_data.work_date,
        )

        department = context.selected_department
        return redirect(f"{reverse('daily_work_list')}?department={department}")

    return render(
        request, "daily_work/daily_work_piecework_create.html", asdict(context)
    )
