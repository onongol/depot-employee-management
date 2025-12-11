from django.utils.translation import gettext_lazy as _

from employee.views.wagon.wagon_totals import get_totals


def build_totals_row(qs):
    # Calculate totals  
    totals = get_totals(qs)

    total_str = str(_("Total"))
    empty = ""

    empty_cols = 4

    totals_row = [total_str] + [empty] * empty_cols + [totals['total_amount'], totals['total_time'], totals['total_price']] + [empty]
    
    return totals_row
