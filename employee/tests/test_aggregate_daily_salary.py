from collections import defaultdict
from datetime import date
from decimal import Decimal

import pytest

from employee.tests.factories import DailySalaryFactory, EmployeeFactory
from employee.views.employee_salary.calculation.aggregate_daily_salary import (
    aggregate_daily_salary,
)


@pytest.mark.django_db
def test_aggregate_daily_salary_sums_by_employee_month_year_with_wagon_forced_none():
    employee = EmployeeFactory(money_per_hour=Decimal("100.00"))
    other_employee = EmployeeFactory(money_per_hour=Decimal("50.00"))
    excluded_employee = EmployeeFactory(money_per_hour=Decimal("999.00"))

    DailySalaryFactory(
        employee=employee, hours_per_day=10, salary_date=date(2026, 3, 5)
    )
    DailySalaryFactory(
        employee=employee, hours_per_day=5, salary_date=date(2026, 3, 20)
    )
    # different month -> excluded by the month filter
    DailySalaryFactory(
        employee=employee, hours_per_day=24, salary_date=date(2026, 4, 1)
    )
    DailySalaryFactory(
        employee=other_employee, hours_per_day=4, salary_date=date(2026, 3, 1)
    )
    # not in the `employees` list passed below -> excluded by employee__in
    DailySalaryFactory(
        employee=excluded_employee, hours_per_day=24, salary_date=date(2026, 3, 1)
    )

    salary_data = defaultdict(dict)
    aggregate_daily_salary(
        salary_data=salary_data,
        employees=[employee, other_employee],
        month=3,
        year=2026,
    )

    assert salary_data[(employee.pk, 2026, 3, None)]["total_salary_day"] == Decimal(
        "1500.00"
    )
    assert salary_data[(other_employee.pk, 2026, 3, None)][
        "total_salary_day"
    ] == Decimal("200.00")
    assert (excluded_employee.pk, 2026, 3, None) not in salary_data
