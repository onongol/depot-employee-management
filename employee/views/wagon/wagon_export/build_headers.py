from django.utils.translation import gettext_lazy as _


def build_headers(context):
    month_group = context.month_group

    if month_group:
        headers = [
            ("#"),
            _("Wagon Number"),
            _("Wagon Type"),
            _("Total Time"),
            _("Total Price"),
            _("Month"),
            _("Year"),
        ]
    else:
        headers = [
            ("#"),
            _("Wagon Number"),
            _("Wagon Type"),
            _("Work Name"),
            _("Work Type"),
            _("Amount"),
            _("Total Time"),
            _("Total Price"),
            _("Date"),
        ]

    headers = [str(h) for h in headers]

    return headers
