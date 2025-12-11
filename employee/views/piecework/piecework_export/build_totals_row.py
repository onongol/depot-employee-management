from django.utils.translation import gettext_lazy as _

from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS


def build_totals_row(qs, department):
    """Build totals row for DailyWork export based on department."""
    total_str = str(_("Total"))
    empty = ""

    show_wagon = department in ALLOWED_WAGON_DEPARTMENTS
    empty_cols = 8 if show_wagon else 6

    # Calculate totals
    total_amount = sum(pw.amount or 0 for pw in qs) if qs else 0
    total_time = sum(pw.amount_time or 0 for pw in qs) if qs else 0
    total_price = sum(pw.amount_price or 0 for pw in qs) if qs else 0

    totals_row = [total_str] + [empty] * empty_cols + [total_amount, total_time, total_price] + [empty]
    
    return totals_row
