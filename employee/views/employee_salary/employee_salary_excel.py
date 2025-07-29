# Example usage for employee salaries:
from .employee_salary_filtered import get_filtered_employee_salaries
from employee.utils.export_excel import export_to_excel


def employee_salary_export_excel(request):
    """Export employee salaries data to Excel."""
    employee_salaries = get_filtered_employee_salaries(request)

    headers = [
        "Employee ID", "Name", "Department", "Job Title", "Month", "Year",
        "Base Salary", "Piecework Amount", "Total Salary"
    ]
    
    data = [
        [
            item['employee'].employee_id or "",
            item['employee'].name or "",
            item['employee'].department or "",
            item['employee'].job_title or "",
            item['month'] or "",
            item['year'] or "",
            item['total_salary_day'] or 0,
            item['total_piecework_amount'] or 0,
            item['total_salary'] or 0,
        ]
        for item in employee_salaries
    ]

    return export_to_excel(data, headers, "employee_salaries.xlsx", "Employee Salaries")
