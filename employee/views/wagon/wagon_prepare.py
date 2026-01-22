from employee.constants.constants import DEFAULT_WAGON_NUMBER
from employee.models import DailyWork
from employee.utils.month_period import parse_month_period
from employee.utils.select_department import get_selected_department


def wagon_prepare(request):
    """
    Centralizes parsing of GET params and building the base DailyWork queryset for wagon pages/exports,
    so views can reuse the same inputs before applying filters, grouping, sorting, and pagination.
    """
    department = get_selected_department(request)

    wagon_number = request.GET.get("wagon_number", "").strip()
    type_wagon = request.GET.get("type_wagon")
    work_name = request.GET.get("work")
    type_work = request.GET.get("type_work")
    range_date = request.GET.get("range_date")

    group = request.GET.get("group")
    month, year, month_period = parse_month_period(request)

    order_by = request.GET.get("order_by")
    direction = request.GET.get("direction")

    # Base queryset for dailyworks related to wagons
    dailyworks = (
        DailyWork.objects.select_related("work")
        .exclude(wagon_number__isnull=True)
        .exclude(wagon_number=DEFAULT_WAGON_NUMBER)
    )

    # Filter by selected department (was missing)
    if department:
        dailyworks = dailyworks.filter(work__department=department)

    return (
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
    )
