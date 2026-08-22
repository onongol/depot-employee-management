from datetime import date
from decimal import Decimal

from employee.tests.factories import EmployeeFactory
from employee.views.daily_salary.daily_salary_create.daily_salary_build_instances import (
    build_daily_salary_instances,
)


def test_build_daily_salary_instances_skips_duplicate_employee():
    duplicate_employee = EmployeeFactory.build(
        employee_id=1, money_per_hour=Decimal("100.00")
    )
    new_employee = EmployeeFactory.build(
        employee_id=2, money_per_hour=Decimal("100.00")
    )
    employees_dict = {1: duplicate_employee, 2: new_employee}

    new_records, errors = build_daily_salary_instances(
        selected_ids=[1, 2],
        employees_dict=employees_dict,
        existing_records={1},  # employee 1 already has a record for this date
        salary_date=date(2026, 3, 5),
        hours_per_day=8,
    )

    assert len(errors) == 1
    assert [record.employee_code for record in new_records] == [2]
