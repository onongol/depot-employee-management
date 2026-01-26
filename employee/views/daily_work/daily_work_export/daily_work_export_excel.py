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
    show_wagon = dw_context.show_wagon
    month_group = dw_context.month_group
    year_group = dw_context.year_group

    daily_works = filter_daily_works(daily_works, context=dw_context)

    daily_works = group_and_sort_daily_works(daily_works, context=dw_context)

    headers = build_headers(
        show_wagon=show_wagon, month_group=month_group, year_group=year_group
    )

    data = list(
        iter_rows(
            daily_works,
            show_wagon=show_wagon,
            month_group=month_group,
            year_group=year_group,
        )
    )

    data.append(
        build_totals_row(
            daily_works,
            show_wagon=show_wagon,
            month_group=month_group,
            year_group=year_group,
        )
    )

    meta = {
        GROUP_MONTH: ("monthly_work.xlsx", _("Monthly Work")),
        GROUP_YEAR: ("yearly_work.xlsx", _("Yearly Work")),
    }

    file_name, title = meta.get(dw_context.group, ("daily_work.xlsx", _("Daily Work")))
    sheet_title = str(title)

    return export_to_excel(data, headers, file_name, sheet_title)
