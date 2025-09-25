from employee.models import Piecework
from employee.utils.filters import filter_wagon
from employee.constants.constants import DEFAULT_WAGON_NUMBER


def wagon_prepare(request):
    """Prepare the base queryset and filter parameters for wagons."""
    wagon_number = request.GET.get('wagon_number', '').strip()
    work_name = request.GET.get('work')
    work_date = request.GET.get('work_date')

    pieceworks = Piecework.objects.select_related('work').filter(
        employee__is_active=True,
    ).exclude(wagon_number__isnull=True).exclude(wagon_number=DEFAULT_WAGON_NUMBER)

    return pieceworks, wagon_number, work_name, work_date


def wagon_filter(request):
    """Filtered wagon data for export."""
    pieceworks, wagon_number, work_name, work_date = wagon_prepare(request)

    pieceworks = filter_wagon(
        pieceworks,
        wagon_number=wagon_number,
        work_name=work_name,
        work_date=work_date
    )

    return pieceworks, wagon_number, work_name, work_date
