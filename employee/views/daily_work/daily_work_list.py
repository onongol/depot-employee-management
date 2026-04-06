from dataclasses import asdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from employee.constants.constants import (
    ALLOWED_WAGON_DEPARTMENTS,
    GROUP_MONTH,
    GROUP_YEAR,
)
from employee.utils.filters import filter_daily_works
from employee.utils.pagination import paginate_queryset
from employee.utils.totals_for_group import calc_totals_for_group
from employee.views.daily_work.daily_work_prepare import daily_work_prepare
from employee.views.daily_work.group.group_and_sort import group_and_sort_daily_works


@login_required()
def daily_work_list(request):
    """List daily work entries with filtering and pagination."""
    context = daily_work_prepare(request)

    daily_works = context.daily_works

    daily_works = filter_daily_works(daily_works, context=context)
    totals = calc_totals_for_group(
        daily_works,
        context=context,
        date_field="work_date",
    )

    daily_works = group_and_sort_daily_works(daily_works, context=context)

    page_obj = paginate_queryset(request, daily_works)

    return render(
        request,
        "daily_work/daily_work_list.html",
        {
            **asdict(context),
            "rows": page_obj,
            "page_obj": page_obj,
            "totals": totals,
            "ALLOWED_WAGON_DEPARTMENTS": ALLOWED_WAGON_DEPARTMENTS,
            "GROUP_MONTH": GROUP_MONTH,
            "GROUP_YEAR": GROUP_YEAR,
        },
    )
