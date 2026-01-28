from decimal import Decimal

from django.utils.translation import gettext_lazy as _


def validate_parse_amount(amount, work, errors):
    """
    Checks the presence and validity of the amount value.
    If invalid, adds an error to errors and returns None.
    If valid, returns Decimal(amount).
    """
    work_name = work.work_name

    if not amount:
        errors.append(
            _("Amount required for work %(work_name)s.") % {"work_name": work_name}
        )
        return None
    try:
        return Decimal(amount)
    except Exception:
        errors.append(
            _("Invalid amount for work %(work_name)s.") % {"work_name": work_name}
        )
        return None
