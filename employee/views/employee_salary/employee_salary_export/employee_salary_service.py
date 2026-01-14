from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS, GROUP_WAGON
from employee.utils.filters import filter_employees
from employee.views.employee_salary.employee_salary_calculate import employee_salary_calculate
from employee.views.employee_salary.employee_salary_prepare import employee_salaries_prepare
from employee.views.employee_salary.employee_salary_sort import apply_ordering


def get_employee_salaries(request):
    (
        employees, 
        employee_id, 
        employee_name, 
        department, 
        job_title,
        wagon_number, 
        month, 
        year, 
        month_period, 
        group, 
        order_by, 
        direction,
        wagon_mode
    ) = employee_salaries_prepare(request)

    employees = filter_employees(
        employees, 
        department=department, 
        employee_id=employee_id, 
        employee_name=employee_name, 
        job_title=job_title
    )
   
    employee_salaries = employee_salary_calculate(
        employees, 
        month, 
        year, 
        group_by_wagon=wagon_mode,
        wagon_number=wagon_number if wagon_mode else None
    )

    apply_ordering(
        employee_salaries,
        order_by,
        direction,
        allowed_fields=["employee_id", "month", "year"],
    )

    return employee_salaries, group, wagon_mode
