from employee.models import DailyWork
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

    # Base queryset for dailyworks related to wagons
    dailyworks = (
        DailyWork.objects
        .select_related('work')
        .exclude(wagon_number__isnull=True)
        .exclude(wagon_number=DEFAULT_WAGON_NUMBER)
    )

    # Filter by selected department (was missing)
    if department:
        dailyworks = dailyworks.filter(work__department=department)

    return dailyworks, wagon_number, work_name, work_date, department


def wagon_filter(request):
    """Filtered wagon data for export."""
    dailyworks, wagon_number, work_name, work_date, department = wagon_prepare(request)

    dailyworks = filter_wagon(
        dailyworks,
        wagon_number=wagon_number,
        work_name=work_name,
        work_date=work_date
    )

    return dailyworks, wagon_number, work_name, work_date, department
