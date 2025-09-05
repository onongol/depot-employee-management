from django.db.models import Sum, Max, F, FloatField, ExpressionWrapper
from collections import defaultdict

from .wagon_filtered import wagon_filtered, get_grouped_wagon_data
from employee.utils.export_excel import export_to_excel


def export_wagon_excel(request):
    """Export wagon data to Excel."""
    pieceworks = wagon_filtered(request)

    wagon_data = get_grouped_wagon_data(pieceworks)

    # Группировка как во views
    grouped = defaultdict(lambda: {'amount': 0, 'total_price': 0, 'total_time': 0})
    for row in wagon_data:
        key = (row['wagon_number'], row['work__work_name'], row['work_date'], row['type_work'])
        grouped[key]['amount'] += row['amount']
        grouped[key]['total_price'] += row['total_price']
        grouped[key]['total_time'] += row['total_time']

    grouped_wagon_data = [
        [
            k[0],  # wagon_number
            k[3],  # type_work
            k[1],  # work__work_name
            v['amount'],
            v['total_time'],
            v['total_price'],
            k[2],  # work_date
        ]
        for k, v in grouped.items()
    ]

    
    total_amount = sum(row[3] for row in grouped_wagon_data)
    total_time = sum(row[4] for row in grouped_wagon_data)
    total_price = sum(row[5] for row in grouped_wagon_data)

    headers = [
        "Wagon Number", "Type Work", "Work Name", "Amount", "Total Time", "Total Price", "Date",
    ]

    # Добавить итоговую строку
    grouped_wagon_data.append(["Total", "", "", total_amount, total_time, total_price, ""])

    return export_to_excel(grouped_wagon_data, headers, "wagon.xlsx", "Wagon")