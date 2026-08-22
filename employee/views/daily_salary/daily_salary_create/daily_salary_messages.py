from django.contrib import messages
from django.utils.translation import gettext as _


def send_daily_salary_creation_message(
    request, *, employees_dict, selected_ids, salary_date, template: str | None = None
):
    """
    Send a success message for created DailySalary records.
    - employees_dict: mapping employee_id -> Employee instance
    - selected_ids: list of employee_ids attempted to create
    - salary_date: date string
    """
    if template is None:
        template = _("Created records for %(employees)s - %(date)s")

    employee_list = [
        str(emp) for emp_id, emp in employees_dict.items() if emp_id in selected_ids
    ]

    employees_str = ", ".join(sorted(employee_list)) if employee_list else ""

    messages.success(
        request, template % {"employees": employees_str, "date": salary_date}
    )
