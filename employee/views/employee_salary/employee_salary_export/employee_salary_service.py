from employee.utils.filters import filter_employees
from employee.views.employee_salary.calculation.calculate_employee_salaries import (
    calculate_employee_salaries,
)
from employee.views.employee_salary.employee_salary_prepare import (
    employee_salaries_prepare,
)
from employee.views.employee_salary.employee_salary_sort import apply_ordering


def get_employee_salaries(request):
    context = employee_salaries_prepare(request)

    employees = context.employees

    employees = filter_employees(employees, context=context)

    employee_salaries = calculate_employee_salaries(
        employees,
        context=context,
        wagon_number=context.wagon_number if context.wagon_mode else None,
    )

    apply_ordering(
        employee_salaries,
        context=context,
        allowed_fields=["employee_id", "month", "year"],
    )

    return employee_salaries, context
