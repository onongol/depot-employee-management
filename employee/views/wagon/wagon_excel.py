from django.utils.translation import gettext_lazy as _

from employee.utils.export_excel import export_to_excel
from .wagon_filtered import wagon_filter
from .wagon_grouping import get_grouped_wagon_data, get_totals

def export_wagon_excel(request):
    """Export wagon data to Excel."""
    dailyworks, wagon_number, work_name, work_date, department = wagon_filter(request)

    wagon_data = get_grouped_wagon_data(dailyworks)

    # Calculate totals  
    totals = get_totals(dailyworks)

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
        for row in wagon_data
    ]

    total_str = _("Total")
    total_str = str(total_str)

    # Append totals row
    data.append([total_str, "", "", totals['total_amount'], totals['total_time'], totals['total_price'], ""])

    file_name = "wagon.xlsx"

    sheet_title = _("Wagon")
    sheet_title = str(sheet_title)

    return export_to_excel(data, headers, file_name, sheet_title)
