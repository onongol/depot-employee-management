from employee.utils.filters import filter_employees
from .employee_salary_prepare import employee_salaries_prepare
from .employee_salary_calculate import employee_salary_calculate


def get_filtered_employee_salaries(request):
    """Return a list of filtered employee salaries based on request parameters."""
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
