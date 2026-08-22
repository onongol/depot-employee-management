from django.utils.translation import gettext_lazy as _


def build_headers():
    headers = [
        ("#"),
        _("Material"),
        _("Work Name"),
        _("Amount"),
        _("Date"),
    ]

    return [str(h) for h in headers]
