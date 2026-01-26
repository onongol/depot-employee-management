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
    pw_context = piecework_prepare(request)

    pieceworks = pw_context.pieceworks
    department = pw_context.selected_department

    safe_department = (department or "all").replace(" ", "_")

    pieceworks = filter_pieceworks(pieceworks, context=pw_context)

    pieceworks = group_and_sort_pieceworks(pieceworks, context=pw_context)

    headers = build_headers(context=pw_context)

    data = list(iter_rows(pieceworks, context=pw_context))

    data.append(build_totals_row(pieceworks, context=pw_context))

    meta = {
        GROUP_MONTH: ("monthly_piecework", _("Monthly Piecework")),
        GROUP_YEAR: ("yearly_piecework", _("Yearly Piecework")),
    }

    file_name, title = meta.get(pw_context.group, ("piecework", _("Piecework")))
    file_name = f"{file_name}_{safe_department}.xlsx"
    sheet_title = f"{title} ({department})"

    return export_to_excel(data, headers, file_name, sheet_title)
