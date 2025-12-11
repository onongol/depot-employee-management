from django.utils.translation import gettext_lazy as _


def build_headers():
    headers = [
        _("#"),
        _("ID"),
        _("Name"),
        _("Department"),
        _("Position"),
        _("Rank"),
        #_("Month Salary"),
        _("Time"),
        _("Salary"),
        #_("Total Salary"),
        _("Month"),
        _("Year"),
    ]

    headers = [str(h) for h in headers]

    return headers
