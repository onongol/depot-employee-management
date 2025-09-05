from employee.utils.export_excel import export_to_excel
from .wagon_filtered import wagon_filter
from .wagon_grouping import get_grouped_wagon_data, regroup_and_sum_wagon_data


def export_wagon_excel(request):
    """Export wagon data to Excel."""
    pieceworks, wagon_number, work_name, work_date = wagon_filter(request)

    wagon_data = get_grouped_wagon_data(pieceworks)

    # Group and sum by wagon_number, work__work_name, work_date. Convert grouped dict to list for export
    grouped_wagon_data, total_amount, total_time, total_price = regroup_and_sum_wagon_data(wagon_data)

    # Format data for export to Excel
    export_data = [
        [
            row['wagon_number'],
            row['type_work'],
            row['work__work_name'],
            row['amount'],
            row['total_time'],
            row['total_price'],
            row['work_date'],
        ]
        for row in grouped_wagon_data
    ]

    headers = [
        "Wagon Number", "Type Work", "Work Name", "Amount", "Total Time", "Total Price", "Date",
    ]

    # Add totals row
    export_data.append(["Total", "", "", total_amount, total_time, total_price, ""])

    return export_to_excel(export_data, headers, "wagon.xlsx", "Wagon")