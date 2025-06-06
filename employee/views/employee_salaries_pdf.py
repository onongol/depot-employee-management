from employee.views.export_pdf import export_to_pdf
from employee.views.filtered_employee_salaries import get_filtered_employee_salaries


def export_employee_salaries_pdf(request):
    """Export employee salaries data to PDF."""
    employee_salaries = get_filtered_employee_salaries(request)

    headers = [
        "ID", "Name", "Department", "Job Title", "Rank", "Salary Month", "Total Piecework", "Total Salary", "Month", "Year"
    ]
    col_widths = [40, 100, 120, 120, 40, 100, 100, 100, 40, 40]
    
    data = [
        [
            item['employee'].employee_id,
            item['employee'].name,
            item['employee'].department,
            item['employee'].job_title,
            item['employee'].rank,
            item['total_salary_day'],
            item['total_piecework_amount'],
            item['total_salary'],
            item['month'],
            item['year'],
        ]
        for item in employee_salaries
    ]

    col_alignments = [
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),   # ID column centered
        ('ALIGN', (1, 1), (3, -1), 'LEFT'),     # Name, Department, Job Title left-aligned
        ('ALIGN', (4, 1), (4, -1), 'CENTER'),   # Rank column centered
        ('ALIGN', (5, 1), (7, -1), 'RIGHT'),    # Salary Month, Total Piecework, Total Salary right-aligned
        ('ALIGN', (8, 1), (9, -1), 'CENTER'),     # Month and Year centered
    ]

    return export_to_pdf(data, headers, col_widths, col_alignments, "Employee Salaries", "employee_salaries.pdf")
