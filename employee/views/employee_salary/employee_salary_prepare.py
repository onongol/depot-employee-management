from employee.models import Employee
from employee.utils.group_modes import is_wagon_group, is_detail_group
from employee.utils.month_period import parse_month_period
from employee.utils.select_department import get_selected_department
from employee.utils.selects import get_distinct_values
from employee.utils.wagon_department import is_wagon_department
from employee.views.employee_salary.employee_salary_context import EmployeeSalaryContext


def employee_salaries_prepare(request) -> EmployeeSalaryContext:
    """Prepare the base queryset and filter parameters for employee salaries."""
    department = get_selected_department(request)

    # Limit the base queryset by user role: employees see only their own record; admins/managers see all active employees.
    if request.user.groups.filter(name="Employees").exists():
        employees = Employee.objects.filter(user=request.user, is_active=True)
    else:
        employees = Employee.objects.filter(is_active=True)

    employee_id = request.GET.get("employee_id", "")
    employee_name = request.GET.get("employee_name", "")
    job_title = request.GET.get("job_title", "")
    wagon_number = (request.GET.get("wagon_number") or "").strip()

    group = (request.GET.get("group") or "").strip()
    month, year, month_period = parse_month_period(request)

    order_by = (request.GET.get("order_by") or "").strip()
    direction = (request.GET.get("direction") or "").strip()

    show_wagon = is_wagon_department(department)
    total_group = is_detail_group(group)
    wagon_group = is_wagon_group(group)
    wagon_mode = wagon_group and show_wagon

    # Get distinct values for dropdown filters
    job_titles = get_distinct_values(
        Employee,
        "job_title",
        department,
        department_field="department",
        only_with_salary=True,
    )

    return EmployeeSalaryContext(
        employees=employees,
        employee_id=employee_id,
        employee_name=employee_name,
        selected_department=department,
        job_title=job_title,
        wagon_number=wagon_number,
        month=month,
        year=year,
        month_period=month_period,
        group=group,
        order_by=order_by,
        direction=direction,
        show_wagon=show_wagon,
        total_group=total_group,
        wagon_group=wagon_group,
        wagon_mode=wagon_mode,
        job_titles=job_titles,
    )
