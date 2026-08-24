from decimal import Decimal
from types import SimpleNamespace

from employee.views.daily_work.daily_work_create.calculation.calculate_salary_percentages import (
    calculate_salary_percentages,
)


def _salary(employee_id, salary_day):
    return SimpleNamespace(
        employee=SimpleNamespace(employee_id=employee_id),
        salary_day=Decimal(salary_day),
    )


def test_calculate_salary_percentages_splits_by_share_of_total_rounding_half_up():
    employees_salary = [_salary(1, "1"), _salary(2, "31")]

    percentages = calculate_salary_percentages(employees_salary)

    assert percentages == {1: Decimal("3.13"), 2: Decimal("96.88")}


def test_calculate_salary_percentages_zero_total_returns_unquantized_zero():
    employees_salary = [_salary(1, "0"), _salary(2, "0")]

    percentages = calculate_salary_percentages(employees_salary)

    assert percentages == {1: Decimal("0"), 2: Decimal("0")}
    assert str(percentages[1]) == "0"
