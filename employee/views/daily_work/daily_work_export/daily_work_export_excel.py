from django.utils.translation import gettext_lazy as _

from employee.utils.exports.export_excel import export_to_excel
from employee.utils.filters import filter_daily_works
from employee.views.daily_work.daily_work_export.build_headers import build_headers
from employee.views.daily_work.daily_work_export.build_totals_row import build_totals_row
from employee.views.daily_work.daily_work_export.daily_work_prepare import daily_work_prepare
from employee.views.daily_work.daily_work_export.format_data import iter_rows


def daily_work_export_excel(request):
    """Export filtered DailyWork list to Excel."""
    # Prepare data
    (
        daily_works,
        department,
        job_title,
        work_name,
        type_work,
        wagon_number,
        type_wagon,
        type_material,
        range_date,
        record_date,
    ) = daily_work_prepare(request)

    # Apply all filters using a reusable filter function
    daily_works = filter_daily_works(
        daily_works,
        job_title=job_title,
        work_name=work_name,
        type_work=type_work,
        wagon_number=wagon_number,
        type_wagon=type_wagon,
        type_material=type_material,
        range_date=range_date,
        record_date=record_date
    )

    # Sort in descending order
    daily_works = daily_works.order_by('-work_date', '-record_date')

    # Build headers
    headers = build_headers(department)

    # Format data for Excel
    data = list(iter_rows(daily_works, department))

    # Append totals row
    data.append(build_totals_row(daily_works, department))

    file_name = "daily_work.xlsx"
    sheet_title = str(_("Daily Work"))

    return export_to_excel(data, headers, file_name, sheet_title)
