from django.urls import reverse
from django.utils import timezone

from employee.forms import DailySalaryForm
from employee.models import DailySalary, Employee
from employee.utils.select_department import get_selected_department
from employee.utils.selects import get_distinct_values
from employee.views.daily_salary.daily_salary_create.daily_salary_create_context import (
    DailySalaryCreateContext,
)


def prepare_daily_salary_create(request) -> DailySalaryCreateContext:
    """Build context for daily salary creation view."""
    department = get_selected_department(request)

    today = timezone.now().date()

    # Filter employees by selected department, or show none if not selected
    employees = []
    if department:
        employees = list(
            Employee.objects.filter(department=department, is_active=True).order_by(
                "employee_id"
            )
        )

    # Get distinct job titles for filtering dropdown
    job_titles = get_distinct_values(Employee, "job_title", department)

    # Fetch existing DailySalary records for the department to prevent duplicates
    existing_daily_salaries = list(
        DailySalary.objects.filter(department=department).values(
            "employee_code", "salary_date"
        )
    )

    return DailySalaryCreateContext(
        form=DailySalaryForm(),
        object_type="Daily Salary",
        employees=employees,
        today=today,
        selected_department=department,
        cancel_url=reverse("daily_salary_list"),
        job_titles=job_titles,
        existing_daily_salaries=existing_daily_salaries,
    )
