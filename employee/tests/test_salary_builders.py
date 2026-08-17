from decimal import Decimal
from types import SimpleNamespace

from employee.views.employee_salary.calculation.salary_builders import (
    build_employee_salary_list,
)


def _employee(pk, department="Засвар 1"):
    return SimpleNamespace(pk=pk, department=department)


def test_build_employee_salary_list_combines_totals_for_known_employee():
    employee = _employee(pk=1)
    salary_data = {
        (1, 2026, 3, None): {
            "total_salary_day": Decimal("1000.00"),
            "total_piecework_amount": Decimal("250.00"),
            "total_piecework_time": Decimal("5.5"),
        }
    }

    rows = build_employee_salary_list(salary_data=salary_data, employees=[employee])

    assert len(rows) == 1
    row = rows[0]
    assert row["employee"] is employee
    assert row["department"] == "Засвар 1"
    assert row["wagon_number"] is None
    assert row["month"] == 3
    assert row["year"] == 2026
    assert row["total_salary_day"] == Decimal("1000.00")
    assert row["total_piecework_amount"] == Decimal("250.00")
    assert row["total_salary"] == Decimal("1250.00")


def test_build_employee_salary_list_skips_rows_for_unknown_employee():
    # salary_data can reference an employee id that isn't in `employees`
    # (e.g. filtered out upstream); that row must be dropped, not KeyError.
    known_employee = _employee(pk=1)
    salary_data = {
        (1, 2026, 3, None): {"total_salary_day": Decimal("1000.00")},
        (999, 2026, 3, None): {"total_salary_day": Decimal("500.00")},
    }

    rows = build_employee_salary_list(
        salary_data=salary_data, employees=[known_employee]
    )

    assert len(rows) == 1
    assert rows[0]["employee"] is known_employee


def test_build_employee_salary_list_defaults_missing_totals_to_zero():
    # e.g. the caller skips aggregate_daily_salary (include_daily_salary=False),
    # so salary_data only carries piecework totals for this key.
    employee = _employee(pk=1)
    salary_data = {(1, 2026, 3, None): {"total_piecework_amount": Decimal("250.00")}}

    rows = build_employee_salary_list(salary_data=salary_data, employees=[employee])

    row = rows[0]
    assert row["total_salary_day"] == 0
    assert row["total_piecework_time"] == 0
    assert row["total_salary"] == Decimal("250.00")
