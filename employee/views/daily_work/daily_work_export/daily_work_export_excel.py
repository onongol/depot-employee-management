from django.utils.translation import gettext_lazy as _

from employee.constants.constants import GROUP_MONTH, GROUP_YEAR
from employee.utils.exports.export_excel import export_to_excel
from employee.utils.filters import filter_daily_works
from employee.views.daily_work.daily_work_export.build_headers import build_headers
from employee.views.daily_work.daily_work_export.build_totals_row import (
    build_totals_row,
)
from employee.views.daily_work.daily_work_export.format_data import iter_rows
from employee.views.daily_work.daily_work_prepare import daily_work_prepare
from employee.views.daily_work.group.group_and_sort import group_and_sort_daily_works


def daily_work_export_excel(request):
    """Export filtered DailyWork list to Excel."""
    dw_context = daily_work_prepare(request)

    daily_works = dw_context.daily_works
    department = dw_context.selected_department

    safe_department = (department or "all").replace(" ", "_")

    daily_works = filter_daily_works(daily_works, context=dw_context)

    daily_works = group_and_sort_daily_works(daily_works, context=dw_context)

    headers = build_headers(context=dw_context)

    data = list(iter_rows(daily_works, context=dw_context))

    data.append(build_totals_row(daily_works, context=dw_context))

    meta = {
        GROUP_MONTH: ("monthly_work", _("Monthly Work")),
        GROUP_YEAR: ("yearly_work", _("Yearly Work")),
    }

    file_name, title = meta.get(dw_context.group, ("daily_work", _("Daily Work")))
    file_name = f"{file_name}_{safe_department}.xlsx"
    sheet_title = f"{title} ({department})"

    return export_to_excel(data, headers, file_name, sheet_title)
