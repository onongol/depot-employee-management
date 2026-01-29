from employee.utils.filters import filter_employees_salary
from employee.views.employee_salary.calculation.calculate_employee_salaries import (
    calculate_employee_salaries,
)
from employee.views.employee_salary.employee_salary_prepare import (
    employee_salaries_prepare,
)
from employee.views.employee_salary.employee_salary_sort import apply_ordering


def get_employee_salaries(request):
    es_context = employee_salaries_prepare(request)

    employees = es_context.employees

    employees = filter_employees_salary(
        employees,
        context=es_context
    )

    employee_salaries = calculate_employee_salaries(
        employees,
        context=es_context,
        wagon_number=es_context.wagon_number if es_context.wagon_mode else None,
    )

    apply_ordering(
        employee_salaries,
        context=es_context,
        allowed_fields=["employee_id", "month", "year"],
    )

    return employee_salaries, es_context
