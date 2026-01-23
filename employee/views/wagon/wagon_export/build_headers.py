from django.utils.translation import gettext_lazy as _


def build_headers(month_group=None):
    if month_group:
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
