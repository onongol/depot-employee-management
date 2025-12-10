from django.utils.translation import gettext_lazy as _

from .employee_salary_filtered import get_filtered_employee_salaries
from employee.utils.export_pdf import export_to_pdf


def employee_salary_export_pdf(request):
    """Export employee salaries data to PDF."""
    employee_salaries = get_filtered_employee_salaries(request)

    headers = [
        _("#"),
        _("ID"),
        _("Name"),
        _("Department"),
        _("Position"),
        _("Rank"),
        _("Time"),
        #_("Month Salary"),
        _("Salary"),
        #_("Total Salary"),
        _("Month"),
        _("Year"),
    ]
    
    headers = [str(h) for h in headers]

    # A4 Landscape ~842pt; usable width ~800pt
    col_widths = [30, 30, 150, 150, 150, 50, 50, 100, 50, 50]
    
    data = [
        [   
            i + 1,
            item['employee'].employee_id or "",
            item['employee'].name or "",
            item['employee'].department or "",
            item['employee'].job_title or "",
            item['employee'].rank or "",
            item['total_piecework_time'] or 0,
            #item['total_salary_day'] or 0,
            item['total_piecework_amount'] or 0,
            #item['total_salary'] or 0,
            item['month'] or "",
            item['year'] or "",
        ]
        for i, item in enumerate(employee_salaries)
    ]

    # Define column alignments
    col_alignments = [
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),     # #
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),     # ID 
        ('ALIGN', (2, 1), (4, -1), 'LEFT'),     # Name, Department, Job Title 
        ('ALIGN', (5, 1), (5, -1), 'LEFT'),     # Rank 
        ('ALIGN', (6, 1), (7, -1), 'LEFT'),     # Time, Salary  
        ('ALIGN', (8, 1), (9, -1), 'LEFT'),     # Month, Year
    ]

    file_name = "employee_salaries.pdf"
    
    sheet_title = _("Employee Salaries")
    sheet_title = str(sheet_title)

    return export_to_pdf(data, headers, col_widths, col_alignments, sheet_title, file_name)
