from employee.models import Piecework
from employee.utils.select_department import get_selected_department

def piecework_prepare(request):
    """Prepare base queryset and filter params for Piecework."""
    department = get_selected_department(request)

    # Base queryset (same visibility rules as list view)
    if request.user.groups.filter(name='Employees').exists():
        pieceworks = Piecework.objects.select_related('employee', 'work').filter(
            employee__user=request.user,
            employee__department=department,
            employee__is_active=True,
        )
    else:
        pieceworks = Piecework.objects.select_related('employee', 'work').filter(
            employee__department=department,
            employee__is_active=True,
        )

    # Extract filter parameters from request
    employee_id = request.GET.get('employee_id')
    employee_name = request.GET.get('employee_name')
    job_title = request.GET.get('job_title')
    work_name = request.GET.get('work_name')
    type_work = request.GET.get('type_work')
    wagon_number = request.GET.get('wagon_number')
    type_wagon = request.GET.get('type_wagon')
    type_material = request.GET.get('type_material')
    range_date = request.GET.get('range_date')
    record_date = request.GET.get('record_date')

    return (
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
    )