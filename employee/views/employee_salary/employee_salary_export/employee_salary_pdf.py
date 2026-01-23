from django.utils.translation import gettext_lazy as _

from employee.constants.constants import GROUP_WAGON
from employee.utils.exports.export_pdf import export_to_pdf
from employee.views.employee_salary.employee_salary_export.build_headers import (
    build_headers,
)
from employee.views.employee_salary.employee_salary_export.employee_salary_service import (
    get_employee_salaries,
)
from employee.views.employee_salary.employee_salary_export.format_data import iter_rows


def employee_salary_export_pdf(request):
    """Export employee salaries data to PDF."""
    employee_salaries, group, wagon_mode = get_employee_salaries(request)

    headers = build_headers(wagon_mode=wagon_mode)

    # A4 Landscape ~842pt;
    columns = ["#", "id", "name", "department", "position", "rank"]
    if wagon_mode:
        columns.append("wagon")
    columns += ["time", "salary", "month", "year"]

    widths_by_key = {
        "#": 30,
        "id": 30,
        "name": 100,
        "department": 150,
        "position": 100,
        "rank": 50,
        "wagon": 80,
        "time": 50,
        "salary": 100,
        "month": 50,
        "year": 50,
    }

    col_widths = [widths_by_key[col] for col in columns]

    # Define column alignments
    last_col = len(col_widths) - 1
    col_alignments = [
        ("ALIGN", (0, 1), (last_col, -1), "LEFT"),
    ]

    data = list(iter_rows(employee_salaries, wagon_mode=wagon_mode))

    meta = {
        GROUP_WAGON: ("employee_salaries_wagon.pdf", _("Employee Salaries by Wagon")),
    }

    file_name, title = meta.get(
        group, ("employee_salaries.pdf", _("Employee Salaries"))
    )
    sheet_title = str(title)

    return export_to_pdf(
        data, headers, col_widths, col_alignments, sheet_title, file_name
    )
