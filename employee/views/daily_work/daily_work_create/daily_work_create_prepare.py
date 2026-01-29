from django.urls import reverse
from django.utils import timezone

from employee.forms import PieceworkForm
from employee.models import Employee, Piecework, Work
from employee.utils.converting_date import format_date
from employee.utils.select_department import get_selected_department
from employee.utils.select_type_wagon import get_type_wagon_filter_values
from employee.utils.selects import get_distinct_values
from employee.views.daily_work.daily_work_create.daily_work_create_context import (
    DailyWorkPieceworkCreateContext,
)


def daily_work_piecework_create_prepare(request) -> DailyWorkPieceworkCreateContext:
    """Build context for daily work and piecework views."""
    department = get_selected_department(request)

    today = timezone.now().date()

    # Get and format the work_date from GET or POST parameters
    raw_work_date = request.GET.get("work_date") or request.POST.get("work_date")
    work_date = format_date(raw_work_date) if raw_work_date else today

    # Fetch employees and works based on the selected department and work_date
    if department:
        employees = Employee.objects.filter(
            department=department, is_active=True
        ).order_by("employee_id")
        works = Work.objects.filter(department=department).order_by("work_name")
        if work_date:
            employees = employees.filter(dailysalary__salary_date=work_date).distinct()
    else:
        employees = Employee.objects.none()
        works = Work.objects.none()

    # Get distinct job titles for filtering dropdown
    emp_job_titles = get_distinct_values(
        Employee, "job_title", department, department_field="department"
    )
    work_job_titles = get_distinct_values(
        Work,
        "job_title",
        extra_filters={"department": department} if department else None,
    )
    job_titles = sorted(set(list(emp_job_titles) + list(work_job_titles)))

    # Get distinct type_wagon for filtering dropdown if department allows wagons
    type_wagons = get_type_wagon_filter_values(department)

    # Fetch existing Piecework records for the department to prevent duplicates
    existing_pieceworks = list(
        Piecework.objects.filter(employee__department=department).values(
            "employee_id", "work_id", "type_work", "work_date", "wagon_number"
        )
    )

    return DailyWorkPieceworkCreateContext(
        form=PieceworkForm(department=department),
        object_type="Daily Work & Piecework",
        employees=employees,
        works=works,
        today=today,
        work_date=work_date,
        selected_department=department,
        cancel_url=reverse("daily_work_list"),
        existing_pieceworks=existing_pieceworks,
        job_titles=job_titles,
        type_wagons=type_wagons,
    )
