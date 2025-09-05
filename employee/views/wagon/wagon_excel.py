from .wagon_filtered import wagon_filtered
from employee.utils.export_excel import export_to_excel
from django.db.models import Sum, Max, F, FloatField, ExpressionWrapper

def export_wagon_excel(request):
    """Export wagon data to Excel."""
    pieceworks = wagon_filtered(request)

    wagon_data = (
        pieceworks
        .values('type_work','wagon_number', 'work__work_name', 'work__standard_time', 'work_date', 'group_id')
        .annotate(
            amount=Max('amount'),
            total_price=Sum('amount_price'),
        )
        .annotate(
            total_time=ExpressionWrapper(
                F('work__standard_time') * F('amount'),
                output_field=FloatField()
            ),
        )
        .order_by('-work_date', 'type_work', 'wagon_number', 'work__work_name', 'group_id')
    )

    headers = [
        "Wagon Number", "Type Work", "Work Name", "Amount", "Total Time", "Total Price", "Date",
    ]

    data = [
        [
            row['wagon_number'] or "",
            row['type_work'] or "",
            row['work__work_name'] or "",
            row['amount'] or 0,
            row['total_time'] or 0,
            row['total_price'] or 0,
            row['work_date'] or "",
        ]
        for row in wagon_data
    ]

    total_amount = sum(row['amount'] or 0 for row in wagon_data)
    total_time = sum(row['total_time'] or 0 for row in wagon_data)
    total_price = sum(row['total_price'] or 0 for row in wagon_data)

    data.append(["", "", "Total", total_amount, total_time, total_price, ""])

    return export_to_excel(data, headers, "wagon.xlsx", "Wagon")