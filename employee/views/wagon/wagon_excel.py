from django.utils.translation import gettext_lazy as _

from employee.utils.export_excel import export_to_excel
from .wagon_filtered import wagon_filter
from .wagon_grouping import get_grouped_wagon_data, regroup_and_sum_wagon_data


def export_wagon_excel(request):
    """Export wagon data to Excel."""
    pieceworks, wagon_number, work_name, work_date, department = wagon_filter(request)

    wagon_data = get_grouped_wagon_data(pieceworks)

    # Group and sum by wagon_number, work__work_name, work_date. Convert grouped dict to list for export
    grouped_wagon_data, total_amount, total_time, total_price = regroup_and_sum_wagon_data(wagon_data)

    headers = [
        _("Wagon Number"),
        _("Type Work"),
        _("Work Name"),
        _("Amount"),
        _("Total Time"),
        _("Total Price"),
        _("Date"),
    ]

    headers = [str(h) for h in headers]

    # Format data for export to Excel
    data = [
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

    total_str = _("Total")
    total_str = str(total_str)

    # Append totals row
    data.append([total_str, "", "", total_amount, total_time, total_price, ""])

    file_name = "wagon.xlsx"

    sheet_title = _("Wagon")
    sheet_title = str(sheet_title)

    return export_to_excel(data, headers, file_name, sheet_title)
