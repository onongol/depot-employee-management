from employee.models import Employee
from employee.utils.month_period import parse_month_period
from employee.utils.select_department import get_selected_department
from employee.views.employee_salary.employee_salary_wagon import is_wagon_group


def employee_salaries_prepare(request):
    """Prepare the base queryset and filter parameters for employee salaries."""
    department = get_selected_department(request)

    employee_id = request.GET.get("employee_id", "")
    employee_name = request.GET.get("employee_name", "")
    job_title = request.GET.get("job_title", "")
    wagon_number = (request.GET.get("wagon_number") or "").strip()

    month, year, month_period = parse_month_period(request)

    group = (request.GET.get("group") or "").strip()
    order_by = (request.GET.get("order_by") or "").strip()
    direction = (request.GET.get("direction") or "").strip()

    # Limit the base queryset by user role: employees see only their own record; admins/managers see all active employees.
    if request.user.groups.filter(name="Employees").exists():
        employees = Employee.objects.filter(user=request.user, is_active=True)
    else:
        employees = Employee.objects.filter(is_active=True)

    wagon_mode = is_wagon_group(department=department, group=group)

    return (
        employees,
        employee_id,
        employee_name,
        department,
        job_title,
        wagon_number,
        month,
        year,
        month_period,
        group,
        order_by,
        direction,
        wagon_mode,
    )
