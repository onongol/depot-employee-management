from django.utils.translation import gettext_lazy as _


def build_headers(show_wagon=False, month_group=None, year_group=None):
    """Build headers for DailyWork export based on department."""
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
