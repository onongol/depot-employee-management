from django.utils.translation import gettext_lazy as _

from employee.constants.constants import GROUP_MONTH, GROUP_YEAR
from employee.utils.exports.export_excel import export_to_excel
from employee.utils.filters import filter_pieceworks
from employee.views.piecework.group.group_and_sort import group_and_sort_pieceworks
from employee.views.piecework.piecework_export.build_headers import build_headers
from employee.views.piecework.piecework_export.build_totals_row import build_totals_row
from employee.views.piecework.piecework_export.format_data import iter_rows
from employee.views.piecework.piecework_prepare import piecework_prepare


def piecework_export_excel(request):
    """Export filtered Piecework queryset to Excel."""
    context = piecework_prepare(request)

    pieceworks = context.pieceworks
    department = context.selected_department

    safe_department = (department or "all").replace(" ", "_")

    pieceworks = filter_pieceworks(pieceworks, context=context)

    pieceworks = group_and_sort_pieceworks(pieceworks, context=context)

    headers = build_headers(context=context)

    data = list(iter_rows(pieceworks, context=context))

    data.append(build_totals_row(pieceworks, context=context))

    meta = {
        GROUP_MONTH: ("monthly_piecework_records", _("Monthly Piecework Records")),
        GROUP_YEAR: ("yearly_piecework_records", _("Yearly Piecework Records")),
    }

    file_name, title = meta.get(context.group, ("daily_piecework_records", _("Daily Piecework Records")))
    file_name = f"{file_name}_{safe_department}.xlsx"
    sheet_title = f"{title} ({department})"

    return export_to_excel(data, headers, file_name, sheet_title)
