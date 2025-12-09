from django.utils.translation import gettext_lazy as _

from employee.utils.export_excel import export_to_excel
from employee.utils.filters import filter_wagon
from .wagon_prepare import wagon_prepare
from .wagon_aggregation import get_grouped_wagon_data, get_totals

def wagon_export_excel(request):
    """Export wagon data to Excel."""
    dailyworks, wagon_number, type_wagon, work_name, type_work, range_date, department = wagon_prepare(request)

    dailyworks = filter_wagon(
        dailyworks,
        wagon_number=wagon_number,
        type_wagon=type_wagon,
        work_name=work_name,
        type_work=type_work,
        range_date=range_date
    )

    wagon_data = get_grouped_wagon_data(dailyworks)

    # Calculate totals  
    totals = get_totals(dailyworks)

    headers = [
        _("#"),
        _("Wagon Number"),
        _("Type Wagon"),
        _("Work Name"),
        _("Type Work"),
        _("Amount"),
        _("Total Time"),
        _("Total Price"),
        _("Date"),
    ]

    headers = [str(h) for h in headers]

    # Format data for export to Excel
    data = [
        [   
            i + 1,
            row['wagon_number'],
            row['type_wagon'],
            row['work__work_name'],
            row['type_work'],
            row['amount'],
            row['total_time'],
            row['total_price'],
            row['work_date'],
        ]
        for i, row in enumerate(wagon_data)
    ]

    total_str = _("Total")
    total_str = str(total_str)
    empty_str = ""

    # Append totals row
    data.append(
        [total_str] + [empty_str] * 4 + [totals['total_amount'], totals['total_time'], totals['total_price']] + [empty_str]
    )

    file_name = "wagon.xlsx"

    sheet_title = _("Wagon")
    sheet_title = str(sheet_title)

    return export_to_excel(data, headers, file_name, sheet_title)
