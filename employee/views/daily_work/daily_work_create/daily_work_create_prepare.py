from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from employee.forms import PieceworkForm
from employee.forms.filter_forms import WorkDateForm
from employee.models import Employee, Piecework, Work
from employee.utils.job_title_choices import build_job_title_choices
from employee.utils.select_department import get_selected_department
from employee.utils.type_wagon_choices import build_type_wagon_choices
from employee.utils.wagon_department import is_wagon_department
from employee.views.daily_work.daily_work_create.daily_work_create_context import (
    DailyWorkPieceworkCreateContext,
)


def daily_work_piecework_create_prepare(request) -> DailyWorkPieceworkCreateContext:
    """Build context for daily work and piecework views."""
    department = get_selected_department(request)

    show_wagon = is_wagon_department(department)

    today = timezone.localdate()

    # Falls back to today so the page never queries with work_date=None, which
    # is SQL IS NULL and would silently empty the duplicate check.
    raw_work_date = request.GET.get("work_date") or request.POST.get("work_date")
    work_date = (
        WorkDateForm.parse({"work_date": raw_work_date}).get("work_date") or today
    )

    employees = []
    works = []

    # Fetch employees and works based on the selected department and work_date
    if department:
        employees_qs = Employee.objects.filter(
            department=department, is_active=True
        ).order_by("employee_id")

        if work_date:
            employees_qs = employees_qs.filter(
                dailysalary__salary_date=work_date
            ).distinct()

        employees = list(employees_qs)
        works = list(Work.objects.filter(department=department).order_by("work_name"))

    # Build filter choices from the already loaded records to avoid extra lookup queries.
    job_titles = build_job_title_choices(employees, works)
    type_wagons = build_type_wagon_choices(works, show_wagon=show_wagon)

    # Fetch existing Piecework records for the department and work date to prevent duplicates
    existing_pieceworks = list(
        Piecework.objects.filter(
            employee__department=department,
            work_date=work_date,
        ).values("employee_code", "work_id", "type_work", "work_date", "wagon_number")
    )

    return DailyWorkPieceworkCreateContext(
        form=PieceworkForm(department=department),
        object_type=_("Daily Work"),
        employees=employees,
        works=works,
        today=today,
        work_date=work_date,
        selected_department=department,
        cancel_url=reverse("daily_work_list"),
        existing_pieceworks=existing_pieceworks,
        job_titles=job_titles,
        type_wagons=type_wagons,
        show_wagon=show_wagon,
    )
