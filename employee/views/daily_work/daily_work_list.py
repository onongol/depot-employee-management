from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from employee.constants.constants import (
    ALLOWED_WAGON_DEPARTMENTS,
    GROUP_MONTH,
    GROUP_YEAR,
)
from employee.models import DailyWork
from employee.utils.filters import filter_daily_works
from employee.utils.pagination import paginate_queryset
from employee.utils.select_type_wagon import get_type_wagon_filter_values
from employee.utils.selects import get_distinct_values
from employee.utils.totals import calc_totals_for_group
from employee.views.daily_work.daily_work_prepare import daily_work_prepare
from employee.views.daily_work.group.group_and_sort import group_and_sort_daily_works


@login_required(login_url="login")
def daily_work_list(request):
    """List daily work entries with filtering and pagination."""
    (
        daily_works,
        department,
        job_title,
        work_name,
        type_work,
        wagon_number,
        type_wagon,
        type_material,
        range_date,
        record_date,
        group,
        selected_year,
        month,
        year,
        month_period,
        order_by,
        direction,
        show_wagon,
    ) = daily_work_prepare(request)

    # Get distinct values for filtering dropdown
    job_titles = get_distinct_values(
        DailyWork, "job_title", department, department_field="work__department"
    )
    type_works = get_distinct_values(
        DailyWork, "type_work", department, department_field="work__department"
    )
    type_materials = get_distinct_values(
        DailyWork,
        "work__type_material",
        department,
        department_field="work__department",
    )

    # Get snapshot values of type_wagon from DailyWork
    type_wagons = get_type_wagon_filter_values(department, source_model="daily_work")

    # Get available years for filtering
    years = [str(d.year) for d in daily_works.dates("work_date", "year", order="DESC")]

    # Apply all filters using a reusable filter function
    daily_works = filter_daily_works(
        daily_works,
        work_name=work_name,
        job_title=job_title,
        type_work=type_work,
        wagon_number=wagon_number,
        type_wagon=type_wagon,
        type_material=type_material,
        range_date=range_date,
        record_date=record_date,
    )

    # Aggregation for totals
    totals = calc_totals_for_group(
        daily_works,
        group=group,
        month=month,
        year=year,
        selected_year=selected_year,
        date_field="work_date",
    )

    # Grouping and sorting
    daily_works = group_and_sort_daily_works(
        daily_works,
        group=group,
        month=month,
        year=year,
        selected_year=selected_year,
        show_wagon=show_wagon,
        order_by=order_by,
        direction=direction,
    )

    page_obj = paginate_queryset(request, daily_works)

    filters = {
        "department": department or "",
        "work_name": work_name or "",
        "job_title": job_title or "",
        "type_work": type_work or "",
        "type_wagon": type_wagon or "",
        "wagon_number": wagon_number or "",
        "type_material": type_material or "",
        "range_date": range_date or "",
        "record_date": record_date or "",
        "group": group or "",
        "month_period": month_period or "",
        "year": selected_year or "",
    }

    return render(
        request,
        "daily_work/daily_work_list.html",
        {
            "ALLOWED_WAGON_DEPARTMENTS": ALLOWED_WAGON_DEPARTMENTS,
            "GROUP_MONTH": GROUP_MONTH,
            "GROUP_YEAR": GROUP_YEAR,
            "work_name": work_name,
            "job_title": job_title,
            "type_work": type_work,
            "type_wagon": type_wagon,
            "wagon_number": wagon_number,
            "type_material": type_material,
            "range_date": range_date,
            "record_date": record_date,
            "daily_works": page_obj,
            "page_obj": page_obj,
            "selected_department": department,
            "type_works": type_works,
            "job_titles": job_titles,
            "type_wagons": type_wagons,
            "type_materials": type_materials,
            "totals": totals,
            "filters": filters,
            "group": group,
            "month_period": month_period,
            "years": years,
            "selected_year": selected_year,
        },
    )
