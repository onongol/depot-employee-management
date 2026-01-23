from django.utils.translation import gettext_lazy as _

from employee.constants.constants import GROUP_WAGON
from employee.utils.exports.export_excel import export_to_excel
from employee.views.employee_salary.employee_salary_export.build_headers import (
    build_headers,
)
from employee.views.employee_salary.employee_salary_export.employee_salary_service import (
    get_employee_salaries,
)
from employee.views.employee_salary.employee_salary_export.format_data import iter_rows


def employee_salary_export_excel(request):
    """Export employee salaries data to Excel."""
    employee_salaries, group, wagon_mode = get_employee_salaries(request)

    headers = build_headers(wagon_mode=wagon_mode)
    data = list(iter_rows(employee_salaries, wagon_mode=wagon_mode))

    meta = {
        GROUP_WAGON: ("employee_salaries_wagon.xlsx", _("Employee Salaries by Wagon")),
    }

    file_name, title = meta.get(
        group, ("employee_salaries.xlsx", _("Employee Salaries"))
    )
    sheet_title = str(title)

    return export_to_excel(data, headers, file_name, sheet_title)
