from employee.models import Piecework
from employee.utils.group_modes import is_detail_group, is_month_group, is_year_group
from employee.utils.month_period import parse_month_period
from employee.utils.select_department import get_selected_department
from employee.utils.select_type_wagon import get_type_wagon_filter_values
from employee.utils.selects import get_distinct_values
from employee.utils.user_roles import is_employee
from employee.utils.wagon_department import is_wagon_department
from employee.views.piecework.piecework_context import PieceworkContext


def piecework_prepare(request) -> PieceworkContext:
    """Prepare base queryset and filter params for Piecework."""
    department = get_selected_department(request)

    # Base queryset (same visibility rules as list view)
    if is_employee(request):
        pieceworks = Piecework.objects.select_related("employee", "work").filter(
            department=department,
            employee__user=request.user,
            employee__is_active=True,
        )
    else:
        pieceworks = Piecework.objects.select_related("employee", "work").filter(
            department=department,
            employee__is_active=True,
        )

    # Filter parameters
    employee_id = request.GET.get("employee_id")
    employee_code = request.GET.get("employee_code")
    employee_name = request.GET.get("employee_name")
    job_title = request.GET.get("job_title")
    work_name = request.GET.get("work_name")
    type_work = request.GET.get("type_work")
    wagon_number = request.GET.get("wagon_number")
    type_wagon = request.GET.get("type_wagon")
    range_date = request.GET.get("range_date")
    record_date = request.GET.get("record_date")

    # Grouping parameters
    group = request.GET.get("group")
    selected_year = (request.GET.get("year") or "").strip()
    month, year, month_period = parse_month_period(request)

    # Sorting parameters
    order_by = request.GET.get("order_by")
    direction = request.GET.get("direction")

    # Derived flags for UI and logic
    show_wagon = is_wagon_department(department)
    detail_group = is_detail_group(group)
    month_group = is_month_group(group)
    year_group = is_year_group(group)

    # Get distinct values for dropdown filters
    job_titles = get_distinct_values(
        Piecework, "job_title", department, department_field="department"
    )
    type_works = get_distinct_values(
        Piecework, "type_work", department, department_field="department"
    )

    # Get available wagon types for filter dropdown
    type_wagons = get_type_wagon_filter_values(department, source_model="piecework")

    # Get available years for year filter dropdown
    years = get_distinct_values(
        Piecework, "work_year", department, department_field="department"
    )

    return PieceworkContext(
        pieceworks=pieceworks,
        selected_department=department,
        employee_id=employee_id,
        employee_code=employee_code,
        employee_name=employee_name,
        job_title=job_title,
        work_name=work_name,
        type_work=type_work,
        wagon_number=wagon_number,
        type_wagon=type_wagon,
        range_date=range_date,
        record_date=record_date,
        group=group,
        selected_year=selected_year,
        month=month,
        year=year,
        month_period=month_period,
        order_by=order_by,
        direction=direction,
        show_wagon=show_wagon,
        detail_group=detail_group,
        month_group=month_group,
        year_group=year_group,
        job_titles=job_titles,
        type_works=type_works,
        type_wagons=type_wagons,
        years=years,
    )
