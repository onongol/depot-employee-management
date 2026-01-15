from django.utils.translation import gettext_lazy as _

from employee.constants.constants import GROUP_MONTH


def build_headers(group=None):
    if group == GROUP_MONTH:
        headers = [
            ("#"),
            _("Wagon Number"),
            _("Type Wagon"),
            _("Total Time"),
            _("Total Price"),
            _("Month"),
            _("Year"),
        ]
    else:
        headers = [
            ("#"),
            _("Wagon Number"),
            _("Type Wagon"),
            _("Work Name"),
            _("Type Work"),
            _("Amount"),
            _("Total Time"),
            _("Total Price"),
            _("Date"),
        ]

    headers = [str(h) for h in headers]

    return headers
