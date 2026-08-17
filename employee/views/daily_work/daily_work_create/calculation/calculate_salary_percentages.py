# employee/utils/calculate.py
from decimal import ROUND_HALF_UP, Decimal

TWO = Decimal("0.01")


def calculate_salary_percentages(employees_salary):
    """
    Calculate each employee's percentage share of the total salary;
    if the total is zero, assign 0% to all to avoid division by zero
    """
    total = sum(emp.salary_day for emp in employees_salary)

    if total > 0:
        return {
            emp.employee.employee_id: (emp.salary_day / total * 100).quantize(
                TWO, rounding=ROUND_HALF_UP
            )
            for emp in employees_salary
        }
    else:
        return {emp.employee.employee_id: Decimal("0") for emp in employees_salary}
