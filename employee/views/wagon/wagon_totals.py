from django.db.models import Sum


def get_totals(dailyworks):
    """
    Calculate total amounts, time, and price from the original dailyworks queryset.
    """
    # Define the fields we want to total
    fields = ['total_amount', 'total_time', 'total_price']

    # Aggregate totals for the specified fields
    aggregates = dict(
        total_amount=Sum('amount'),
        total_time=Sum('amount_time'),
        total_price=Sum('amount_price'),
    )

    # Perform aggregation
    totals = dailyworks.aggregate(**aggregates) or {}

    # Return totals with default of 0 if None
    return {field: totals.get(field) or 0 for field in fields}
