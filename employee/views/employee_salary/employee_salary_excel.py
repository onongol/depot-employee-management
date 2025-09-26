# Example usage for employee salaries:
from .employee_salary_filtered import get_filtered_employee_salaries
from employee.utils.export_excel import export_to_excel
from django.utils.translation import gettext_lazy as _


def employee_salary_export_excel(request):
    """Export employee salaries data to Excel."""
    employee_salaries = get_filtered_employee_salaries(request)

    headers = [
        _("Department"),
        _("ID"),
        _("Name"),
        _("Position"),
        _("Month Salary"),
        _("Piecework Salary"),
        _("Total Salary"),
        _("Month"),
        _("Year"),
    ]
    
    headers = [str(h) for h in headers]

    data = [
        [
            item['employee'].department or "",
            item['employee'].employee_id or "",
            item['employee'].name or "",
            item['employee'].job_title or "",
            item['total_salary_day'] or 0,
            item['total_piecework_amount'] or 0,
            item['total_salary'] or 0,
            item['month'] or "",
            item['year'] or "",
        ]
        for item in employee_salaries
    ]

    file_name = "employee_salaries.xlsx"
    sheet_title = _("Employee Salaries")
    sheet_title = str(sheet_title)

    return export_to_excel(data, headers, file_name, sheet_title)
