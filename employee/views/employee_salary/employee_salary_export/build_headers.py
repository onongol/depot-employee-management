from django.utils.translation import gettext_lazy as _


def build_headers(*, wagon_mode: bool = False):
    headers = [
        ("#"),
        _("ID"),
        _("Name"),
        _("Department"),
        _("Position"),
        _("Rank"),
    ]

    if wagon_mode:
        headers += [
            _("Wagon"),
        ]

    headers += [
        _("Time"),
        _("Salary"),
        _("Month"),
        _("Year"),
    ]

    headers = [str(h) for h in headers]
    
    return headers
