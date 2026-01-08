from django.utils.translation import gettext_lazy as _

from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS, GROUP_MONTH, GROUP_YEAR


def build_headers(department, group=None):
    """Build headers for DailyWork export based on department."""
    headers = [
        ("#"),
        _("Work"),
        _("Position"),
        _("Type"),
    ]
    if department in ALLOWED_WAGON_DEPARTMENTS:
        headers += [
            _("Wagon"), 
            _("Type Wagon")
        ]
    headers += [
        _("Amount"), 
        _("Time"), 
        _("Price"), 
    ]

    if group == GROUP_MONTH:
        headers += [_("Month"), _("Year")]
    elif group == GROUP_YEAR:
        headers += [_("Year")]
    else:
        headers += [_("Date")]

    headers = [str(h) for h in headers]

    return headers
