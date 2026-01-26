from dataclasses import asdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from employee.utils.filters import filter_daily_salaries
from employee.utils.pagination import paginate_queryset
from employee.utils.sorting import apply_ordering
from employee.views.daily_salary.daily_salary_prepare import daily_salary_prepare


@login_required(login_url="login")
def daily_salary_list(request):
    """View to list all daily salaries with filtering and pagination."""
    ds_context = daily_salary_prepare(request)

    daily_salaries = ds_context.daily_salaries

    daily_salaries = filter_daily_salaries(daily_salaries, context=ds_context)

    daily_salaries = apply_ordering(
        daily_salaries,
        order_by=ds_context.order_by,
        direction=ds_context.direction,
        allowed_fields=["salary_date", "record_date"],
        default=["-salary_date", "-record_date"],
    )

    page_obj = paginate_queryset(request, daily_salaries)

    return render(
        request,
        "daily_salary/daily_salary_list.html",
        {
            **asdict(ds_context),
            "daily_salaries": page_obj,
            "page_obj": page_obj,
        },
    )
