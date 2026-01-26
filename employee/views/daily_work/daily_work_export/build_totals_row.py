from django.utils.translation import gettext_lazy as _

from employee.utils.sum_field import sum_field


def build_totals_row(qs, context):
    """Build totals row for DailyWork export based on department and grouping."""
    show_wagon = context.show_wagon
    month_group = context.month_group
    year_group = context.year_group
    grouped = month_group or year_group

    total_str = str(_("Total"))
    empty = ""

    # Number of empty columns before totals.
    # 5 if show_wagon: [#, Work, Position, Type, Wagon, Type Wagon]
    # 3 if not:        [#, Work, Position, Type]
    empty_cols = 5 if show_wagon else 3

    # Number of empty columns after totals.
    # 2 if month_group: for example, [Month, Year] columns after totals
    # 1 if not: usually just [Date] or similar
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
