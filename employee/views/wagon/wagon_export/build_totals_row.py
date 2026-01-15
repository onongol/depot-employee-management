from django.utils.translation import gettext_lazy as _

from employee.constants.constants import GROUP_MONTH


def build_totals_row(totals: dict, group=None):
    total_str = str(_("Total"))
    empty = ""

    total_amount = totals.get("total_amount") or 0
    total_time = totals.get("total_time") or 0
    total_price = totals.get("total_price") or 0

    if group == GROUP_MONTH:
        empty_cols = 2
        tail_empties = 2
        totals_cells = [total_time, total_price]
    else:
        empty_cols = 4
        tail_empties = 1
        totals_cells = [total_amount, total_time, total_price]

    totals_row = (
        [total_str] 
        + [empty] * empty_cols 
        + totals_cells 
        + [empty] * tail_empties
    )
    
    return totals_row
