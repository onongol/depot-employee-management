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
    (
        dailyworks,
        wagon_number,
        type_wagon,
        work_name,
        type_work,
        range_date,
        department,
        group,
        month,
        year,
        month_period,
        order_by,
        direction,
        month_group,
    ) = wagon_prepare(request)

    # Get distinct type_wagon and type_work for filter options
    type_wagons = dailyworks.values_list("type_wagon", flat=True).distinct()
    type_works = dailyworks.values_list("type_work", flat=True).distinct()

    dailyworks = filter_wagon(
        dailyworks,
        wagon_number=wagon_number,
        type_wagon=type_wagon,
        work_name=work_name,
        type_work=type_work,
        range_date=range_date,
    )

    totals = calc_totals_for_group(
        dailyworks,
        group=group,
        month=month,
        year=year,
        date_field="work_date",
    )

    wagon_data = group_and_sort_wagons(
        dailyworks,
        month_group=month_group,
        month=month,
        year=year,
        order_by=order_by,
        direction=direction,
    )

    page_obj = paginate_queryset(request, wagon_data)

    filters = {
        "wagon_number": wagon_number or "",
        "type_wagon": type_wagon or "",
        "work_name": work_name or "",
        "type_work": type_work or "",
        "range_date": range_date or "",
        "department": department or "",
        "group": group or "",
        "month_period": month_period or "",
    }

    return render(
        request,
        "wagon/wagon_list.html",
        {
            "GROUP_MONTH": GROUP_MONTH,
            "wagon_number": wagon_number,
            "type_wagon": type_wagon,
            "work_name": work_name,
            "type_work": type_work,
            "range_date": range_date,
            "wagon_data": wagon_data,
            "rows": page_obj,
            "page_obj": page_obj,
            "selected_wagon": wagon_number,
            "selected_department": department,
            "total_amount": totals["total_amount"],
            "total_time": totals["total_time"],
            "total_price": totals["total_price"],
            "type_wagons": type_wagons,
            "type_works": type_works,
            "filters": filters,
            "group": group,
            "month_period": month_period,
            "month_group": month_group,
        },
    )
