from employee.utils.filters import filter_employees
from employee.views.employee_salary.employee_salary_calculate import employee_salary_calculate
from employee.views.employee_salary.employee_salary_prepare import employee_salaries_prepare


def get_employee_salaries(request):
    # Prepare the base queryset and filter parameters
    employees, employee_id, employee_name, department, job_title, month, year, month_period = employee_salaries_prepare(request)

    # Apply filters to the employee queryset using reusable filter functions
    employees = filter_employees(
        employees, 
        department=department, 
        employee_id=employee_id, 
        employee_name=employee_name, 
        job_title=job_title
    )

    # Calculate salaries for the filtered employees
    employee_salaries = employee_salary_calculate(employees, month, year)

    # Sort by year and month descending (newest first)
    employee_salaries.sort(key=lambda x: (x['year'], x['month']), reverse=True)

    return employee_salaries
