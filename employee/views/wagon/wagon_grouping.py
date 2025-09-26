from django.db.models import Sum, F, FloatField, ExpressionWrapper, Max
from collections import defaultdict


def get_grouped_wagon_data(pieceworks):
    """
    View to list all wagons with related works, amount, total time, price, and date.
    """
    wagon_data = (
        pieceworks
        .values('type_work','wagon_number', 'work__work_name', 'work__standard_time', 'work_date', 'group_id')
        .annotate(
            amount=Max('amount'),  # Only one amount per group (not summed)
            total_price=Sum('amount_price'),  # Sum price for all records in the group
        )
        .annotate(
            total_time=ExpressionWrapper(
                F('work__standard_time') * F('amount'),
                output_field=FloatField()
            ),
        )
        .order_by('-work_date', 'type_work', 'wagon_number', 'work__work_name', 'group_id')
    )

    return wagon_data


def regroup_and_sum_wagon_data(wagon_data):
    """
    Groups and sums wagon_data by wagon_number, work__work_name, work_date, type_work.
    Returns: (grouped_wagon_data, total_amount, total_time, total_price)
    """
    grouped = defaultdict(lambda: {'amount': 0, 'total_price': 0, 'total_time': 0})
    for row in wagon_data:
        key = (row['wagon_number'], row['work__work_name'], row['work_date'], row['type_work'])
        grouped[key]['amount'] += row['amount']
        grouped[key]['total_price'] += row['total_price']
        grouped[key]['total_time'] += row['total_time']

    grouped_wagon_data = [
        {
            'wagon_number': k[0],
            'work__work_name': k[1],
            'work_date': k[2],
            'type_work': k[3],
            'amount': v['amount'],
            'total_price': v['total_price'],
            'total_time': v['total_time'],
        }
        for k, v in grouped.items()
    ]

    total_amount = sum(row['amount'] for row in grouped_wagon_data)
    total_time = sum(row['total_time'] for row in grouped_wagon_data)
    total_price = sum(row['total_price'] for row in grouped_wagon_data)

    return grouped_wagon_data, total_amount, total_time, total_price
