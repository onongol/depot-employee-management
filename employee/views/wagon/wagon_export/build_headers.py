from django.utils.translation import gettext_lazy as _


def build_headers():
    headers = [
        _("#"),
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
