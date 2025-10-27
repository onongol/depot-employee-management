from django.db.models import Sum, F, FloatField, ExpressionWrapper, Max
from collections import defaultdict


def get_grouped_wagon_data(dailyworks):
    """
    View to list all wagons with related works, amount, total time, price, and date.
    """
    wagon_data = (
        dailyworks
        .values('work__work_name', 'type_work', 'wagon_number', 'type_wagon', 'work_date')
        .annotate(
            amount=Sum('amount'),
            total_time=Sum('amount_time'),
            total_price=Sum('amount_price'),
        )
        .order_by('-work_date', 'work__work_name', 'type_work', 'wagon_number', 'type_wagon')
    )

    return wagon_data


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
