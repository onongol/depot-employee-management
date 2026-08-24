from datetime import date
from decimal import Decimal

import pytest

from employee.models import DailySalary
from employee.tests.factories import EmployeeFactory


@pytest.mark.django_db
def test_daily_salary_save_computes_salary_day_from_hours_and_rate():
    employee = EmployeeFactory(money_per_hour=Decimal("2500.50"))

    daily_salary = DailySalary(
        employee=employee, hours_per_day=8, salary_date=date(2026, 3, 5)
    )
    daily_salary.save()

    assert daily_salary.salary_day == Decimal("20004.00")


def test_daily_salary_save_raises_value_error_when_employee_has_no_hourly_rate():
    # No @pytest.mark.django_db: the guard raises before super().save() ever
    # touches the database, so an unsaved in-memory Employee is enough.
    employee = EmployeeFactory.build(money_per_hour=None)
    daily_salary = DailySalary(
        employee=employee, hours_per_day=8, salary_date=date(2026, 3, 5)
    )

    # This is a bare ValueError, not a Django ValidationError, so a
    # ModelForm's form.save() won't turn it into a field error for the user
    # — it propagates as an unhandled exception (500) instead.
    with pytest.raises(ValueError, match="hourly rate is not set"):
        daily_salary.save()
