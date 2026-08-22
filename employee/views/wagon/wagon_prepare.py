from employee.constants.constants import DEFAULT_WAGON_NUMBER
from employee.models import DailyWork
from employee.utils.group_modes import is_detail_group, is_month_group
from employee.utils.month_period import parse_month_period
from employee.utils.select_department import get_selected_department
from employee.utils.select_type_wagon import get_type_wagon_filter_values
from employee.utils.selects import get_distinct_values
from employee.views.wagon.wagon_context import WagonContext


def wagon_prepare(request) -> WagonContext:
    """
    Centralizes parsing of GET params and building the base DailyWork queryset for wagon pages/exports,
    so views can reuse the same inputs before applying filters, grouping, sorting, and pagination.
    """
    department = get_selected_department(request)

    # Base queryset for dailyworks related to wagons
    daily_works = (
        DailyWork.objects.select_related("work")
        .exclude(wagon_number__isnull=True)
        .exclude(wagon_number=DEFAULT_WAGON_NUMBER)
    )

    # Filter by selected department (was missing)
    if department:
        daily_works = daily_works.filter(department=department)

    wagon_number = request.GET.get("wagon_number", "").strip()
    type_wagon = request.GET.get("type_wagon")
    work_name = request.GET.get("work")
    type_work = request.GET.get("type_work")
    range_date = request.GET.get("range_date")

    group = request.GET.get("group")
    month, year, month_period = parse_month_period(request)

    order_by = request.GET.get("order_by")
    direction = request.GET.get("direction")

    detail_group = is_detail_group(group)
    month_group = is_month_group(group)

    # Get distinct type_wagon and type_work for filter options
    type_wagons = get_type_wagon_filter_values(department, source_model="daily_work")
    type_works = get_distinct_values(DailyWork, "type_work", department)

    return WagonContext(
        daily_works=daily_works,
        selected_department=department,
        wagon_number=wagon_number,
        type_wagon=type_wagon,
        work_name=work_name,
        type_work=type_work,
        range_date=range_date,
        group=group,
        month=month,
        year=year,
        month_period=month_period,
        order_by=order_by,
        direction=direction,
        detail_group=detail_group,
        month_group=month_group,
        type_wagons=list(type_wagons),
        type_works=list(type_works),
    )
