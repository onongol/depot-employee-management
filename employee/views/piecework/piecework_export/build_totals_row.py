from django.utils.translation import gettext_lazy as _

from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS, GROUP_MONTH, GROUP_YEAR
from employee.utils.sum_field import sum_field


def build_totals_row(qs, department, group=None):
    total_str = str(_("Total"))
    empty = ""
    show_wagon = department in ALLOWED_WAGON_DEPARTMENTS
    empty_cols = 8 if show_wagon else 6
    is_grouped = group in (GROUP_MONTH, GROUP_YEAR)
    tail_empties = 2 if group == GROUP_MONTH else 1

    amount_key, time_key, price_key = (
        ("total_amount", "total_time", "total_price")
        if is_grouped
        else ("amount", "amount_time", "amount_price")
    )

    rows = list(qs) if qs is not None else []

    if not rows:
        total_amount = total_time = total_price = 0
    else:
        total_amount = sum_field(rows, amount_key)
        total_time = sum_field(rows, time_key)
        total_price = sum_field(rows, price_key)

    totals_row = [total_str] + [empty] * empty_cols + [total_amount, total_time, total_price] + [empty] * tail_empties
    
    return totals_row
