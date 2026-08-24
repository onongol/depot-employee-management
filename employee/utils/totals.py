from django.db.models import Sum


def calc_totals(qs):
    """Return totals for raw (non-grouped) queryset."""
    return qs.aggregate(
        total_amount=Sum("amount"),
        total_time=Sum("amount_time"),
        total_price=Sum("amount_price"),
    )
