from django.utils.translation import gettext_lazy as _

from employee.utils.group_modes import is_month_group, is_year_group
from employee.utils.wagon_department import is_wagon_department


def build_headers(department, group=None):
    """Build headers for DailyWork export based on department."""
    show_wagon = is_wagon_department(department)
    month_group = is_month_group(group)
    year_group = is_year_group(group)

    headers = [
        ("#"),
        _("Work"),
        _("Position"),
        _("Type"),
    ]

    if show_wagon:
        headers += [_("Wagon"), _("Type Wagon")]

    headers += [
        _("Amount"),
        _("Time"),
        _("Price"),
    ]

    if month_group:
        headers += [_("Month"), _("Year")]
    elif year_group:
        headers += [_("Year")]
    else:
        headers += [_("Date")]

    headers = [str(h) for h in headers]

    return headers
