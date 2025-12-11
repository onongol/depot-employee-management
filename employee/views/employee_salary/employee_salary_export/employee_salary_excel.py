from django.utils.translation import gettext_lazy as _

from .employee_salary_service import get_employee_salaries
from .build_headers import build_headers
from .format_data import iter_rows
from employee.utils.export_excel import export_to_excel


def employee_salary_export_excel(request):
    """Export employee salaries data to Excel."""
    employee_salaries = get_employee_salaries(request)

    headers = build_headers()
    
    data = list(iter_rows(employee_salaries))

    file_name = "employee_salaries.xlsx"
    sheet_title = str(_("Employee Salaries"))

    return export_to_excel(data, headers, file_name, sheet_title)
