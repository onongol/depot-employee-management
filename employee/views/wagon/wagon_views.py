from dataclasses import asdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from employee.constants.constants import GROUP_MONTH
from employee.utils.filters import filter_wagon
from employee.utils.pagination import paginate_queryset
from employee.utils.totals_for_group import calc_totals_for_group
from employee.views.wagon.group.group_and_sort import group_and_sort_wagons
from employee.views.wagon.wagon_prepare import wagon_prepare


@login_required(login_url="login")
def wagon_list(request):
    """
    Lists wagon-related DailyWork rows. The view:
    1) calls wagon_prepare() to parse GET params and build the base queryset,
    2) applies filters (filter_wagon),
    3) groups/sorts results (group_and_sort_wagons),
    4) paginates and renders the table.
    This keeps request parsing and queryset setup consistent across the list and exports.
    """
    context = wagon_prepare(request)

    daily_works = context.daily_works

    daily_works = filter_wagon(daily_works, context=context)

    totals = calc_totals_for_group(
        daily_works,
        context=context,
        date_field="work_date",
    )

    wagon_data = group_and_sort_wagons(daily_works, context=context)

    page_obj = paginate_queryset(request, wagon_data)

    return render(
        request,
        "wagon/wagon_list.html",
        {
            **asdict(context),
            "wagon_data": wagon_data,
            "rows": page_obj,
            "page_obj": page_obj,
            "total_amount": totals["total_amount"],
            "total_time": totals["total_time"],
            "total_price": totals["total_price"],
            "GROUP_MONTH": GROUP_MONTH,
        },
    )
