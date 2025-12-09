from django.utils.translation import gettext_lazy as _

from employee.utils.filters import filter_pieceworks
from employee.utils.export_excel import export_to_excel
from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS
from .piecework_prepare import piecework_prepare


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

    # Headers
    headers = [
        _("#"),
        _("ID"),
        _("Name"),
        _("Department"),
        _("Position"),
        _("Work"),
        _("Type"),
    ]
    
    # Add wagon-related headers conditionally
    if department in ALLOWED_WAGON_DEPARTMENTS:
        headers += [
            _("Wagon"), 
            _("Type Wagon")
        ]

    headers += [
        _("Amount"), 
        _("Time"), 
        _("Price"), 
        _("Date")
    ]

    headers = [str(h) for h in headers]

    # Order pieceworks by date
    pieceworks = pieceworks.order_by('-work_date', '-record_date')

    # Format data for Excel
    data = []

    for pw in pieceworks:
        row = [
            len(data) + 1,
            pw.employee.employee_id or "",
            pw.employee.name or "",
            pw.department or "",
            pw.job_title or "",
            pw.work.work_name or "",
            pw.type_work or "",
        ]
        if department in ALLOWED_WAGON_DEPARTMENTS:
            row.append(pw.wagon_number_display or "")
            row.append(pw.type_wagon_display or "")
        row.extend([
            pw.amount or 0,
            pw.amount_time or 0,
            pw.amount_price or 0,
            pw.work_date or "",
        ])
        
        data.append(row)

    # Calculate total amounts
    total_amount = sum(pw.amount or 0 for pw in pieceworks) if pieceworks else 0
    total_amount_time = sum(pw.amount_time or 0 for pw in pieceworks) if pieceworks else 0
    total_amount_price = sum(pw.amount_price or 0 for pw in pieceworks) if pieceworks else 0

    total_str = _("Total")
    total_str = str(total_str)
    empty_row = ""

    # Determine number of empty columns based on department
    empty_cols = 8 if department in ALLOWED_WAGON_DEPARTMENTS else 6

    data.append(
        [total_str] + [empty_row] * empty_cols + [total_amount, total_amount_time, total_amount_price] + [empty_row]
    )

    file_name = "piecework.xlsx"

    sheet_title = str(_("Piecework"))   

    return export_to_excel(data, headers, file_name, sheet_title)
