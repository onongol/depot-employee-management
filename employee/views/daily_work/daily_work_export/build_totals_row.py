from django.utils.translation import gettext_lazy as _

from employee.utils.group_modes import is_grouped, is_month_group
from employee.utils.sum_field import sum_field
from employee.utils.wagon_department import is_wagon_department


def build_totals_row(qs, department, group=None):
    """Build totals row for DailyWork export based on department and grouping."""
    total_str = str(_("Total"))
    empty = ""

    show_wagon = is_wagon_department(department)
    empty_cols = 5 if show_wagon else 3  # Work/Position/Type + (optional wagon cols)

    month_group = is_month_group(group)
    grouped = is_grouped(group)

    tail_empties = 2 if month_group else 1

    amount_key, time_key, price_key = (
        ("total_amount", "total_time", "total_price")
        if grouped
        else ("amount", "amount_time", "amount_price")
    )

    # Fetch all rows to handle both QuerySet and list inputs
    rows = list(qs) if qs is not None else []

    if not rows:
        total_amount = total_time = total_price = 0
    else:
        total_amount = sum_field(rows, amount_key)
        total_time = sum_field(rows, time_key)
        total_price = sum_field(rows, price_key)

    totals_row = (
        [total_str]
        + [empty] * empty_cols
        + [total_amount, total_time, total_price]
        + [empty] * tail_empties
    )

    return totals_row
