from employee.models import DailyWork
from employee.constants.constants import DEFAULT_WAGON_NUMBER
from employee.utils.select_department import get_selected_department


def wagon_prepare(request):
    """Prepare the base queryset and filter parameters for wagons."""
    
    # Get the selected department from the request/session
    department = get_selected_department(request)

    wagon_number = request.GET.get('wagon_number', '').strip()
    type_wagon = request.GET.get('type_wagon')
    work_name = request.GET.get('work')
    type_work = request.GET.get('type_work')
    range_date = request.GET.get('range_date')

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

    return dailyworks, wagon_number, type_wagon, work_name, type_work, range_date, department
