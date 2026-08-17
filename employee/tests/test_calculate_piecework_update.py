from decimal import Decimal
from types import SimpleNamespace

from employee.services.calculate_piecework_update import calculate_piecework_update


def _salary(salary_day):
    return SimpleNamespace(salary_day=Decimal(salary_day))


def test_calculate_piecework_update_basic():
    work = SimpleNamespace(price=Decimal("1000.00"))
    daily_salary = _salary("1")
    employees_salary = [_salary("1"), _salary("31")]

    result = calculate_piecework_update(work, Decimal("3"), daily_salary, employees_salary)

    assert result == Decimal("93.90")


def test_calculate_piecework_update_zero_total_salary_avoids_division_by_zero():
    work = SimpleNamespace(price=Decimal("1000.00"))
    daily_salary = _salary("0")

    result = calculate_piecework_update(work, Decimal("3"), daily_salary, employees_salary=[])

    assert result == Decimal("0.00")


def test_calculate_piecework_update_none_amount_returns_unquantized_zero():
    work = SimpleNamespace(price=Decimal("1000.00"))
    daily_salary = _salary("1")
    employees_salary = [_salary("1"), _salary("31")]

    result = calculate_piecework_update(work, None, daily_salary, employees_salary)

    assert str(result) == "0"
