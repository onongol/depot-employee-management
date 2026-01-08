from django.utils.translation import gettext_lazy as _

from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS, GROUP_MONTH, GROUP_YEAR


def _get(item, key, default=0):
    """Helper to get value from dict or object."""
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)


def build_totals_row(qs, department, group=None):
    """Build totals row for DailyWork export based on department and grouping."""
    total_str = str(_("Total"))
    empty = ""

    show_wagon = department in ALLOWED_WAGON_DEPARTMENTS
    empty_cols = 5 if show_wagon else 3  # Work/Position/Type + (optional wagon cols)

    is_grouped = group in (GROUP_MONTH, GROUP_YEAR)

    if is_grouped:
        total_amount = sum((_get(dw, "total_amount", 0) or 0) for dw in qs) if qs else 0
        total_time = sum((_get(dw, "total_time", 0) or 0) for dw in qs) if qs else 0
        total_price = sum((_get(dw, "total_price", 0) or 0) for dw in qs) if qs else 0
        tail_empties = 2 if group == GROUP_MONTH else 1
    else:
        total_amount = sum((_get(dw, "amount", 0) or 0) for dw in qs) if qs else 0
        total_time = sum((_get(dw, "amount_time", 0) or 0) for dw in qs) if qs else 0
        total_price = sum((_get(dw, "amount_price", 0) or 0) for dw in qs) if qs else 0
        tail_empties = 1

    totals_row = [total_str] + [empty] * empty_cols + [total_amount, total_time, total_price] + [empty] * tail_empties
    return totals_row
