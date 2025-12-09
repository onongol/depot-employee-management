from django.utils.translation import gettext_lazy as _

from .employee_salary_filtered import get_filtered_employee_salaries
from employee.utils.export_excel import export_to_excel


def employee_salary_export_excel(request):
    """Export employee salaries data to Excel."""
    employee_salaries = get_filtered_employee_salaries(request)

    headers = [
        _("#"),
        _("ID"),
        _("Name"),
        _("Department"),
        _("Position"),
        #_("Month Salary"),
        _("Salary"),
        #_("Total Salary"),
        _("Month"),
        _("Year"),
    ]
    
    headers = [str(h) for h in headers]

    data = [
        [
            i + 1,
            item['employee'].employee_id or "",
            item['employee'].name or "",
            item['employee'].department or "",
            item['employee'].job_title or "",
            #item['total_salary_day'] or 0,
            item['total_piecework_amount'] or 0,
            #item['total_salary'] or 0,
            item['month'] or "",
            item['year'] or "",
        ]
        for i, item in enumerate(employee_salaries)
    ]

    file_name = "employee_salaries.xlsx"
    
    sheet_title = _("Employee Salaries")
    sheet_title = str(sheet_title)

    return export_to_excel(data, headers, file_name, sheet_title)
