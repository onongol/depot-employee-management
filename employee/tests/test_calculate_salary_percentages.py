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


def test_calculate_salary_percentages_splits_by_share_of_total():
    employees_salary = [_salary(1, "1"), _salary(2, "31")]

    percentages = calculate_salary_percentages(employees_salary)

    assert percentages == {1: Decimal("3.13"), 2: Decimal("96.88")}


def test_calculate_salary_percentages_rounds_half_up_not_half_even():
    # 1/32 * 100 = 3.125 exactly: ROUND_HALF_UP -> 3.13, but Python's round()
    # (banker's rounding) would give 3.12 since 2 is even. This pins the fix
    # in 3758fbf7 that replaced round() with Decimal.quantize(ROUND_HALF_UP)
    # to match calculate_piecework_update.
    employees_salary = [_salary(1, "1"), _salary(2, "31")]

    percentages = calculate_salary_percentages(employees_salary)

    assert percentages[1] == Decimal("3.13")


def test_calculate_salary_percentages_zero_total_returns_unquantized_zero():
    employees_salary = [_salary(1, "0"), _salary(2, "0")]

    percentages = calculate_salary_percentages(employees_salary)

    assert percentages == {1: Decimal("0"), 2: Decimal("0")}
    assert str(percentages[1]) == "0"
