from typing import Iterable, Mapping

from django.contrib import messages
from django.utils.translation import gettext as _

from employee.models import Employee


def send_daily_work_piecework_created(request, *, results: Iterable[Mapping], works_dict: Mapping, work_date, template: str | None = None):
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

    # Collect unique employee ids and names from DB (fallback to 'employee_name' in results)
    employee_ids = [r['employee_id'] for r in results if r.get('employee_id')]
    employees_map = {
        e.employee_id: e.name for e in Employee.objects.filter(employee_id__in=employee_ids)
    }

    employee_entries = sorted({
        f"{r['employee_id']}/{employees_map.get(r['employee_id'], r.get('employee_name', ''))}"
        for r in results
        if r.get('employee_id')
    })

    work_names = sorted({
        works_dict.get(str(r['work_id'])).work_name
        for r in results
        if str(r.get('work_id')) in works_dict
    })

    employees_str = ', '.join(employee_entries)
    works_str = ', '.join(work_names)

    messages.success(
        request,
        template % {'employees': employees_str, 'works': works_str, 'date': work_date}
    )
