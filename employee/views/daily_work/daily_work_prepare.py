from employee.models import DailyWork
from employee.utils.group_modes import is_detail_group, is_month_group, is_year_group
from employee.utils.month_period import parse_month_period
from employee.utils.select_department import get_selected_department
from employee.utils.select_type_wagon import get_type_wagon_filter_values
from employee.utils.select_years import get_years_filter_values
from employee.utils.selects import get_distinct_values
from employee.utils.wagon_department import is_wagon_department
from employee.views.daily_work.daily_work_context import DailyWorkContext


def daily_work_prepare(request) -> DailyWorkContext:
    """Prepare base queryset and filter params for DailyWork export/list."""
    department = get_selected_department(request)

    # Build base queryset filtered by department
    daily_works = DailyWork.objects.filter(department=department).select_related("work")

    # Filter parameters
    job_title = request.GET.get("job_title")
    work_name = request.GET.get("work_name")
    type_work = request.GET.get("type_work")
    wagon_number = request.GET.get("wagon_number")
    type_wagon = request.GET.get("type_wagon")
    type_material = request.GET.get("type_material")
    range_date = request.GET.get("range_date")
    record_date = request.GET.get("record_date")

    # Grouping params
    group = request.GET.get("group")
    raw_year = (request.GET.get("year") or "").strip()
    selected_year = raw_year if raw_year.isdigit() else ""
    month, year, month_period = parse_month_period(request)

    # Sorting params
    order_by = request.GET.get("order_by")
    direction = request.GET.get("direction")

    # Derived flags for UI and logic
    show_wagon = is_wagon_department(department)
    detail_group = is_detail_group(group)
    month_group = is_month_group(group)
    year_group = is_year_group(group)

    # Get distinct values for dropdown filters
    job_titles = get_distinct_values(DailyWork, "job_title", department)
    type_works = get_distinct_values(DailyWork, "type_work", department)
    type_materials = get_distinct_values(
        DailyWork,
        "work__type_material",
        department,
    )

    # Get available wagon types for filter dropdown
    type_wagons = get_type_wagon_filter_values(department, source_model="daily_work")

    # Get available years for year filter dropdown
    years = get_years_filter_values(
        daily_works,
        date_field="work_date",
        cache_prefix="daily_work",
        department=department,
    )

    return DailyWorkContext(
        daily_works=daily_works,
        selected_department=department,
        job_title=job_title,
        work_name=work_name,
        type_work=type_work,
        wagon_number=wagon_number,
        type_wagon=type_wagon,
        type_material=type_material,
        range_date=range_date,
        record_date=record_date,
        group=group,
        selected_year=selected_year,
        month=month,
        year=year,
        month_period=month_period,
        order_by=order_by,
        direction=direction,
        show_wagon=show_wagon,
        detail_group=detail_group,
        month_group=month_group,
        year_group=year_group,
        job_titles=job_titles,
        type_works=type_works,
        type_materials=type_materials,
        type_wagons=type_wagons,
        years=years,
    )
