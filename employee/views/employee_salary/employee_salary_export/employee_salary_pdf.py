from django.utils.translation import gettext_lazy as _

from employee.utils.export_pdf import export_to_pdf
from employee.views.employee_salary.employee_salary_export.build_headers import build_headers
from employee.views.employee_salary.employee_salary_export.employee_salary_service import get_employee_salaries
from employee.views.employee_salary.employee_salary_export.format_data import iter_rows


def employee_salary_export_pdf(request):
    """Export employee salaries data to PDF."""
    employee_salaries = get_employee_salaries(request)

    headers = build_headers()

    # A4 Landscape ~842pt; usable width ~810pt
    col_widths = [30, 30, 150, 150, 150, 50, 50, 100, 50, 50]
    
    # Define column alignments
    col_alignments = [
        ('ALIGN', (0, 1), (9, -1), 'LEFT'), # Align all columns to LEFT
    ]

    data = list(iter_rows(employee_salaries))

    file_name = "employee_salaries.pdf"
    sheet_title = str(_("Employee Salaries"))

    return export_to_pdf(data, headers, col_widths, col_alignments, sheet_title, file_name)
