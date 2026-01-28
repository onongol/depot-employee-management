from typing import Iterable, Mapping

from django.contrib import messages
from django.utils.translation import gettext as _

from employee.views.daily_work.daily_work_create.messages.build_employee_entries import (
    build_employee_entries,
)
from employee.views.daily_work.daily_work_create.messages.build_work_names import (
    build_work_names,
)


def success_creation_message(
    request,
    *,
    results: Iterable[Mapping],
    works_dict: Mapping,
    work_date,
    template: str | None = None,
):
    """
    Build and send a standardized success message for created records.
    - results: iterable of dicts with keys 'employee_id' and 'work_id'
    - works_dict: mapping of work_id (str) -> Work instance
    - work_date: display date (string)
    - template: optional gettext template with placeholders: employees, works, date
    """
    if template is None:
        template = _(
            "Daily Work and related Piecework record(s) for %(employees)s (work(s): %(works)s) on %(date)s created successfully."
        )

    employee_entries = build_employee_entries(results)

    work_names = build_work_names(results, works_dict)

    employees_str = ", ".join(employee_entries)
    works_str = ", ".join(work_names)

    messages.success(
        request,
        template % {"employees": employees_str, "works": works_str, "date": work_date},
    )
