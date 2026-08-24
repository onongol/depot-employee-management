from django.utils.translation import gettext_lazy as _


def build_totals_row(totals: dict, context):
    month_group = context.month_group

    total_str = str(_("Total"))
    empty = ""

    total_amount = totals.get("total_amount") or 0
    total_time = totals.get("total_time") or 0
    total_price = totals.get("total_price") or 0

    if month_group:
        empty_cols = 2
        tail_empties = 2
        totals_cells = [total_time, total_price]
    else:
        empty_cols = 4
        tail_empties = 1
        totals_cells = [total_amount, total_time, total_price]

    return [total_str] + [empty] * empty_cols + totals_cells + [empty] * tail_empties
