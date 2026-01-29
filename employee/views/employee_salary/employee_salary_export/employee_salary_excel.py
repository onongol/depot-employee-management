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
    employee_salaries, context = get_employee_salaries(request)

    department = context.selected_department

    safe_department = (department or "all").replace(" ", "_")

    headers = build_headers(context=context)
    data = list(iter_rows(employee_salaries, context=context))

    meta = {
        GROUP_WAGON: ("employee_salaries_wagon", _("Employee Salaries by Wagon")),
    }

    file_name, title = meta.get(
        context.group, ("employee_salaries", _("Employee Salaries"))
    )
    file_name = f"{file_name}_{safe_department}.xlsx"
    sheet_title = f"{title} ({department})"

    return export_to_excel(data, headers, file_name, sheet_title)
