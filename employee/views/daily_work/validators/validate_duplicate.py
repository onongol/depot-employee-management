from django.utils.translation import gettext_lazy as _

from employee.models import Piecework
from employee.services.normalizes import normalize_wagon_number


def validate_duplicate(selected_employee_ids, selected_work_ids, work_date, type_work, wagon_number):
    """Validate that no duplicate Piecework entries exist for the given parameters."""
    errors = []

    if not selected_employee_ids or not selected_work_ids or not work_date or not type_work:
        return errors

    wagon_number = normalize_wagon_number(wagon_number)

    # Check for existing Piecework entries that would duplicate the new ones
    qs = Piecework.objects.filter(
        employee__employee_id__in=selected_employee_ids,
        work_id__in=selected_work_ids,

        type_work=type_work,
        work_date=work_date,
    )
    if wagon_number is None:
        qs = qs.filter(wagon_number__isnull=True)
    else:
        qs = qs.filter(wagon_number=wagon_number)

    if not qs.exists():
        return errors

    # Prepare error message with existing entries
    pairs = {
        f"{pw.employee.employee_id}/{pw.employee.name} — {pw.work.work_name}"
        for pw in qs.select_related("employee", "work")
    }

    errors.append(
        _(
            "Daily Work & Piecework already exists for: %(pairs)s on %(date)s. Creating duplicates is not allowed."
        )
        % {
            "pairs": ", ".join(sorted(pairs)),
            "date": work_date,
        }
    )
    return errors
