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
    # Prepare data
    (
        pieceworks,
        department,
        employee_id,
        employee_name,
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
        month_period,
        order_by,
        direction,
        show_wagon,
        detail_group,
        month_group,
        year_group,
    ) = piecework_prepare(request)

    # Apply filters
    pieceworks = filter_pieceworks(
        pieceworks,
        employee_id=employee_id,
        employee_name=employee_name,
        job_title=job_title,
        work_name=work_name,
        type_work=type_work,
        wagon_number=wagon_number,
        type_wagon=type_wagon,
        type_material=type_material,
        range_date=range_date,
        record_date=record_date,
    )

    pieceworks = group_and_sort_pieceworks(
        pieceworks,
        group=group,
        month=month,
        year=year,
        selected_year=selected_year,
        show_wagon=show_wagon,
        order_by=order_by,
        direction=direction,
    )

    # Build headers
    headers = build_headers(department, group=group)

    # Format data for Excel
    data = list(iter_rows(pieceworks, department, group=group))

    # Append totals row
    data.append(build_totals_row(pieceworks, department, group=group))

    meta = {
        GROUP_MONTH: ("monthly_piecework.xlsx", _("Monthly Piecework")),
        GROUP_YEAR: ("yearly_piecework.xlsx", _("Yearly Piecework")),
    }

    file_name, title = meta.get(group, ("piecework.xlsx", _("Piecework")))
    sheet_title = str(title)

    return export_to_excel(data, headers, file_name, sheet_title)
