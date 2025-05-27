from django.http import HttpResponse
import openpyxl

from employee.views.filtered_employee_salaries import get_filtered_employee_salaries


def export_employee_salaries_excel(request):
    """Export filtered employee salaries to an Excel file."""
    employee_salaries = get_filtered_employee_salaries(request)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Employee Salaries"
    ws.append([
        "Employee ID", "Name", "Department", "Job Title", "Month", "Year",
        "Base Salary", "Piecework Amount", "Total Salary"
    ])

    for item in employee_salaries:
        ws.append([
            item['employee'].employee_id,
            item['employee'].name,
            item['employee'].department,
            item['employee'].job_title,
            item['monthly_salary'].month,
            item['monthly_salary'].year,
            item['monthly_salary'].salary_month,
            item['total_piecework_amount'],
            item['total_salary'],
        ])
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = (
        'attachment; filename=employee_salaries.xlsx'
    )
    wb.save(response)
    
    return response
