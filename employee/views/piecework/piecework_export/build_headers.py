from django.utils.translation import gettext_lazy as _


def build_headers(context):
    show_wagon = context.show_wagon
    month_group = context.month_group
    year_group = context.year_group

    headers = [
        ("#"),
        _("ID"),
        _("Name"),
        _("Department"),
        _("Position"),
        _("Work"),
        _("Work Type"),
    ]

    if show_wagon:
        headers += [_("Wagon Type"), _("Wagon Number")]
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

    return [str(h) for h in headers]
