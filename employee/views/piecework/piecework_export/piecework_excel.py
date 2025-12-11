from django.utils.translation import gettext_lazy as _

from employee.utils.export_excel import export_to_excel
from employee.utils.filters import filter_pieceworks
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
    
    # Sort in descending order
    pieceworks = pieceworks.order_by('-work_date', '-record_date')

    # Build headers
    headers = build_headers(department)

    # Format data for Excel
    data = list(iter_rows(pieceworks, department))

    # Append totals row
    data.append(build_totals_row(pieceworks, department))

    file_name = "piecework.xlsx"
    sheet_title = str(_("Piecework"))   

    return export_to_excel(data, headers, file_name, sheet_title)
