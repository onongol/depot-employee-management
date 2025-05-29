# Example usage for employee salaries:
from employee.views.filtered_employee_salaries import get_filtered_employee_salaries
from employee.views.export_excel import export_to_excel


def export_employee_salaries_excel(request):
    employee_salaries = get_filtered_employee_salaries(request)
    headers = [
        "Employee ID", "Name", "Department", "Job Title", "Month", "Year",
        "Base Salary", "Piecework Amount", "Total Salary"
    ]
    data = [
        [
            item['employee'].employee_id,
            item['employee'].name,
            item['employee'].department,
            item['employee'].job_title,
            item['monthly_salary'].month,
            item['monthly_salary'].year,
            item['monthly_salary'].salary_month,
            item['total_piecework_amount'],
            item['total_salary'],
        ]
        for item in employee_salaries
    ]
    return export_to_excel(data, headers, "employee_salaries.xlsx", "Employee Salaries")
    