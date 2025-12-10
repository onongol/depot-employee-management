from employee.models import DailyWork
from employee.utils.select_department import get_selected_department


def daily_work_prepare(request):
    """Prepare base queryset and filter params for DailyWork export/list."""
    department = get_selected_department(request)

    # Base queryset by department
    dailyworks = DailyWork.objects.filter(work__department=department).select_related('work')

    # Extract filter parameters
    job_title = request.GET.get('job_title')
    work_name = request.GET.get('work_name')
    type_work = request.GET.get('type_work')
    wagon_number = request.GET.get('wagon_number')
    type_wagon = request.GET.get('type_wagon')
    type_material = request.GET.get('type_material')
    range_date = request.GET.get('range_date')
    record_date = request.GET.get('record_date')

    return (
        dailyworks,
        department,
        job_title,
        work_name,
        type_work,
        wagon_number,
        type_wagon,
        type_material,
        range_date,
        record_date,
    )
