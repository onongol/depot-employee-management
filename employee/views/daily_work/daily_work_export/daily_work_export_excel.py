from django.utils.translation import gettext_lazy as _

from employee.constants.constants import GROUP_MONTH, GROUP_YEAR
from employee.utils.exports.export_excel import export_to_excel
from employee.utils.filters import filter_daily_works
from employee.views.daily_work.daily_work_export.build_headers import build_headers
from employee.views.daily_work.daily_work_export.build_totals_row import build_totals_row
from employee.views.daily_work.daily_work_export.daily_work_prepare import daily_work_prepare
from employee.views.daily_work.daily_work_export.format_data import iter_rows
from employee.views.daily_work.group_and_sort import group_and_sort


def daily_work_export_excel(request):
    """Export filtered DailyWork list to Excel."""
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
        group,
        selected_year,
        month,
        year,
        order_by,
        direction,
        show_wagon,
    ) = daily_work_prepare(request)

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

    daily_works = group_and_sort(
        daily_works,
        group=group,
        month=month,
        year=year,
        selected_year=selected_year,
        show_wagon=show_wagon,
        order_by=order_by,
        direction=direction,
    )

    headers = build_headers(department, group=group)

    data = list(iter_rows(daily_works, department, group=group))

    data.append(build_totals_row(daily_works, department, group=group))

    meta = {
        GROUP_MONTH: ("monthly_work.xlsx", _("Monthly Work")),
        GROUP_YEAR: ("yearly_work.xlsx", _("Yearly Work")),
    }

    file_name, title = meta.get(group, ("daily_work.xlsx", _("Daily Work")))
    sheet_title = str(title)

    return export_to_excel(data, headers, file_name, sheet_title)
