from datetime import date
from decimal import Decimal

import pytest

from employee.services.employee_salary_single import (
    get_employee_total_piecework_amount,
    get_employee_total_salary,
    get_employee_total_salary_day,
)
from employee.tests.factories import (
    DailySalaryFactory,
    EmployeeFactory,
    PieceworkFactory,
)


@pytest.mark.django_db
def test_get_employee_total_salary_day_sums_matching_month_and_employee():
    employee = EmployeeFactory(money_per_hour=Decimal("100.00"))
    DailySalaryFactory(
        employee=employee, hours_per_day=10, salary_date=date(2026, 3, 5)
    )
    DailySalaryFactory(
        employee=employee, hours_per_day=8, salary_date=date(2026, 3, 20)
    )
    # noise: different employee, same month
    DailySalaryFactory(hours_per_day=24, salary_date=date(2026, 3, 10))
    # noise: same employee, different month
    DailySalaryFactory(
        employee=employee, hours_per_day=24, salary_date=date(2026, 4, 1)
    )

    total = get_employee_total_salary_day(employee, month=3, year=2026)

    assert total == Decimal("1800.00")


@pytest.mark.django_db
def test_get_employee_total_salary_day_no_records_is_zero():
    employee = EmployeeFactory()

    total = get_employee_total_salary_day(employee, month=3, year=2026)

    assert total == Decimal("0.00")


@pytest.mark.django_db
def test_get_employee_total_piecework_amount_sums_matching_month_and_employee():
    employee = EmployeeFactory()
    PieceworkFactory(
        employee=employee, work_date=date(2026, 3, 5), amount_price=Decimal("300.00")
    )
    PieceworkFactory(
        employee=employee, work_date=date(2026, 3, 20), amount_price=Decimal("150.50")
    )
    # noise: different employee, same month
    PieceworkFactory(work_date=date(2026, 3, 10), amount_price=Decimal("999.00"))
    # noise: same employee, different month
    PieceworkFactory(
        employee=employee, work_date=date(2026, 4, 1), amount_price=Decimal("999.00")
    )

    total = get_employee_total_piecework_amount(employee, month=3, year=2026)

    assert total == Decimal("450.50")


@pytest.mark.django_db
def test_get_employee_total_piecework_amount_no_records_is_zero():
    employee = EmployeeFactory()

    total = get_employee_total_piecework_amount(employee, month=3, year=2026)

    assert total == Decimal("0.00")


@pytest.mark.django_db
def test_get_employee_total_salary_combines_daily_salary_and_piecework():
    employee = EmployeeFactory(money_per_hour=Decimal("100.00"))
    DailySalaryFactory(
        employee=employee, hours_per_day=10, salary_date=date(2026, 3, 5)
    )
    PieceworkFactory(
        employee=employee, work_date=date(2026, 3, 5), amount_price=Decimal("250.00")
    )

    total = get_employee_total_salary(employee, month=3, year=2026)

    assert total == Decimal("1250.00")
