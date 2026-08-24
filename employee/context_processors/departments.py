from django.utils.translation import gettext_lazy as _

from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS, DEPARTMENTS

SORTED_DEPARTMENTS = tuple(sorted(DEPARTMENTS))


def global_departments(request):
    """Context processor to provide a list of distinct departments."""

    departments = SORTED_DEPARTMENTS

    departments_empty_message = None if departments else _("No departments available.")

    return {
        "departments": departments,
        "departments_empty_message": departments_empty_message,
        "ALLOWED_WAGON_DEPARTMENTS": ALLOWED_WAGON_DEPARTMENTS,
        "request": request,
    }
