from django.db.models import Sum


def get_grouped_wagon_data(dailyworks):
    """
    Group wagons with related works, amount, total time, price, and date.
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
