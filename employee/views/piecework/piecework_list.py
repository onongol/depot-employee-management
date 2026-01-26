from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from employee.constants.constants import (
    ALLOWED_WAGON_DEPARTMENTS,
    GROUP_MONTH,
    GROUP_YEAR,
)
from employee.models import Piecework
from employee.utils.filters import filter_pieceworks
from employee.utils.pagination import paginate_queryset
from employee.utils.select_type_wagon import get_type_wagon_filter_values
from employee.utils.selects import get_distinct_values
from employee.utils.totals_for_group import calc_totals_for_group
from employee.views.piecework.group.group_and_sort import group_and_sort_pieceworks
from employee.views.piecework.piecework_prepare import piecework_prepare


@login_required(login_url="login")
def piecework_list(request):
    """View to list all piecework records with filtering and pagination."""
    # Only show pieceworks for employees in the selected department
    (
        pieceworks,
        department,
        employee_id,
        employee_name,
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
        detail_group,
        month_group,
        year_group,
    ) = piecework_prepare(request)

    # Get distinct values for filtering dropdown
    job_titles = get_distinct_values(
        Piecework, "job_title", department, department_field="employee__department"
    )
    type_works = get_distinct_values(
        Piecework, "type_work", department, department_field="work__department"
    )
    type_materials = get_distinct_values(
        Piecework,
        "work__type_material",
        department,
        department_field="work__department",
    )

    # Get snapshot values of type_wagon from Piecework
    type_wagons = get_type_wagon_filter_values(department, source_model="piecework")

    # Years for Yearly filter dropdown
    years = [str(d.year) for d in pieceworks.dates("work_date", "year", order="DESC")]

    # Apply all filters using a reusable filter function
    pieceworks = filter_pieceworks(
        pieceworks,
        employee_id=employee_id,
        employee_name=employee_name,
        job_title=job_title,
        work_name=work_name,
        type_work=type_work,
        wagon_number=wagon_number,
        type_wagon=type_wagon,
        type_material=type_material,
        range_date=range_date,
        record_date=record_date,
    )

    # Aggregation for totals
    totals = calc_totals_for_group(
        pieceworks,
        group=group,
        month=month,
        year=year,
        selected_year=selected_year,
        date_field="work_date",
    )

    pieceworks = group_and_sort_pieceworks(
        pieceworks,
        group=group,
        month=month,
        year=year,
        selected_year=selected_year,
        show_wagon=show_wagon,
        order_by=order_by,
        direction=direction,
    )

    # Paginate the results, 10 records per page
    page_obj = paginate_queryset(request, pieceworks)

    # Prepare current filter values for template context
    filters = {
        "employee_id": employee_id or "",
        "employee_name": employee_name or "",
        "job_title": job_title or "",
        "work_name": work_name or "",
        "type_work": type_work or "",
        "wagon_number": wagon_number or "",
        "type_wagon": type_wagon or "",
        "type_material": type_material or "",
        "range_date": range_date or "",
        "record_date": record_date or "",
        "group": group or "",
        "month_period": month_period or "",
        "year": selected_year or "",
    }

    # Render the template with all context data
    return render(
        request,
        "piecework/piecework_list.html",
        {
            "ALLOWED_WAGON_DEPARTMENTS": ALLOWED_WAGON_DEPARTMENTS,
            "GROUP_MONTH": GROUP_MONTH,
            "GROUP_YEAR": GROUP_YEAR,
            "employee_id": employee_id,
            "employee_name": employee_name,
            "job_title": job_title,
            "work_name": work_name,
            "type_work": type_work,
            "wagon_number": wagon_number,
            "type_wagon": type_wagon,
            "range_date": range_date,
            "record_date": record_date,
            "pieceworks": page_obj,
            "page_obj": page_obj,
            "selected_department": department,
            "type_works": type_works,
            "type_materials": type_materials,
            "job_titles": job_titles,
            "type_wagons": type_wagons,
            "totals": totals,
            "filters": filters,
            "group": group,
            "month_period": month_period,
            "years": years,
            "selected_year": selected_year,
            "show_wagon": show_wagon,
            "detail_group": detail_group,
            "month_group": month_group,
            "year_group": year_group,
        },
    )
