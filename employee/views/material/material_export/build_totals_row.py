from django.utils.translation import gettext_lazy as _


def build_totals_row(qs):
    total_amount = sum(item["amount_material"] for item in qs) if qs else 0

    total_str = str(_("Total"))
    empty = ""

    empty_cols = 2

    return [total_str] + [empty] * empty_cols + [total_amount] + [empty]
