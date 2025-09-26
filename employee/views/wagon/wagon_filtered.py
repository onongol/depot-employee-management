from employee.models import Piecework
from employee.utils.filters import filter_wagon
from employee.constants.constants import DEFAULT_WAGON_NUMBER
from employee.utils.select_department import get_selected_department


def wagon_prepare(request):
    """Prepare the base queryset and filter parameters for wagons."""
    # Get the selected department from the request/session
    department = get_selected_department(request)

    wagon_number = request.GET.get('wagon_number', '').strip()
    work_name = request.GET.get('work')
    work_date = request.GET.get('work_date')

    # Base queryset for pieceworks related to wagons
    pieceworks = (
        Piecework.objects
        .select_related('work')
        .filter(employee__is_active=True,)
        .exclude(wagon_number__isnull=True)
        .exclude(wagon_number=DEFAULT_WAGON_NUMBER)
    )

    # Filter by selected department (was missing)
    if department:
        pieceworks = pieceworks.filter(employee__department=department)

    return pieceworks, wagon_number, work_name, work_date, department


def wagon_filter(request):
    """Filtered wagon data for export."""
    pieceworks, wagon_number, work_name, work_date, department = wagon_prepare(request)

    pieceworks = filter_wagon(
        pieceworks,
        wagon_number=wagon_number,
        work_name=work_name,
        work_date=work_date
    )

    return pieceworks, wagon_number, work_name, work_date, department 
