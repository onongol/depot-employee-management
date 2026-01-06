from django.utils.translation import gettext_lazy as _

from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS


def build_headers(department):
    headers = [
        ("#"),
        _("ID"),
        _("Name"),
        _("Department"),
        _("Position"),
        _("Work"),
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
        _("Date")
    ]

    headers = [str(h) for h in headers]

    return headers
