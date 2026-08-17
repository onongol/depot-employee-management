from datetime import date
from decimal import Decimal

import pytest

from employee.constants.constants import Department, JobTitle
from employee.tests.factories import (
    DailySalaryFactory,
    DailyWorkFactory,
    EmployeeFactory,
    PieceworkFactory,
    WorkFactory,
)


@pytest.mark.django_db
def test_daily_work_save_derives_work_year_month_and_amounts():
    work = WorkFactory(standard_time=Decimal("2.000000"), price=Decimal("500.00"))

    daily_work = DailyWorkFactory(
        work=work, amount=Decimal("3.00"), work_date=date(2026, 3, 5)
    )

    assert daily_work.work_year == 2026
    assert daily_work.work_month == 3
    # Not re-checking the rounding rules here (covered by
    # test_daily_work_calculations.py) — just that save() actually wires
    # amount into the derived fields instead of leaving model defaults.
    assert daily_work.amount_time == Decimal("6.000000")
    assert daily_work.amount_price == Decimal("1500.00")


@pytest.mark.django_db
def test_daily_work_save_resnapshots_work_fields_on_every_save():
    work = WorkFactory(
        work_name="Original Work",
        department=Department.ZASVAR_1.value,
        job_title=JobTitle.GAGNUURCHIN.value,
    )
    daily_work = DailyWorkFactory(
        work=work,
        job_title="",  # falsy -> falls back to work.job_title
        type_wagon="Something else",  # explicit, but always overwritten from work
    )

    assert daily_work.work_name == "Original Work"
    assert daily_work.department == Department.ZASVAR_1.value
    assert daily_work.job_title == JobTitle.GAGNUURCHIN.value
    # type_wagon normalization always passes current=None to normalize_field
    # (unlike job_title), so it's unconditionally replaced by work.type_wagon
    # even when explicitly set beforehand.
    assert daily_work.type_wagon is None

    work.work_name = "Renamed Work"
    work.department = Department.ZASVAR_2.value
    work.save()

    daily_work.job_title = "Custom Title"
    daily_work.save()

    # Snapshot tracks Work's current state, not a value frozen at creation.
    assert daily_work.work_name == "Renamed Work"
    assert daily_work.department == Department.ZASVAR_2.value
    # job_title, unlike type_wagon, keeps an explicitly provided value.
    assert daily_work.job_title == "Custom Title"


@pytest.mark.django_db
def test_daily_work_save_syncs_linked_piecework_amount_price():
    department = Department.ZASVAR_1.value
    work = WorkFactory(department=department, price=Decimal("1000.00"))
    employee = EmployeeFactory(department=department, money_per_hour=Decimal("100.00"))
    other_employee = EmployeeFactory(
        department=department, money_per_hour=Decimal("300.00")
    )
    work_date = date(2026, 3, 5)

    DailySalaryFactory(employee=employee, hours_per_day=1, salary_date=work_date)
    DailySalaryFactory(employee=other_employee, hours_per_day=1, salary_date=work_date)

    daily_work = DailyWorkFactory(
        work=work, amount=Decimal("1.00"), work_date=work_date
    )
    piecework = PieceworkFactory(
        daily_work=daily_work,
        employee=employee,
        work=work,
        work_date=work_date,
        amount=Decimal(
            "5.00"
        ),  # stale/different amount, must be overwritten by the sync
        amount_price=Decimal("0.01"),  # stale value, must be overwritten by the sync
    )
    # A second Piecework linked to the same DailyWork so both employees'
    # DailySalary participate in the percent split calculate_piecework_update does.
    PieceworkFactory(
        daily_work=daily_work,
        employee=other_employee,
        work=work,
        work_date=work_date,
        amount=Decimal("1.00"),
        amount_price=Decimal("0.01"),
    )

    # Re-saving DailyWork (e.g. someone edits it later) must re-sync
    # amount_price on every linked Piecework, not just at creation time.
    daily_work.save()

    piecework.refresh_from_db()

    # sync_single_piecework overwrites Piecework.amount with DailyWork.amount
    # (not just amount_price), so the stale 5.00 becomes 1.00.
    assert piecework.amount == Decimal("1.00")
    # percent = 100/(100+300)*100 = 25.00; value = 1000.00*25/100 = 250.00;
    # amount_price = 250.00 * 1.00 = 250.00
    assert piecework.amount_price == Decimal("250.00")
