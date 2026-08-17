from decimal import Decimal
from types import SimpleNamespace

import pytest

from employee.services.calculate_piecework_update import calculate_piecework_update
from employee.views.daily_work.daily_work_create.calculation.calculate_salary_percentages import (
    calculate_salary_percentages,
)
from employee.views.daily_work.daily_work_create.calculation.calculate_work_amount_price import (
    calculate_work_amount_price,
)


def _salary(employee_id, salary_day):
    return SimpleNamespace(
        employee=SimpleNamespace(employee_id=employee_id),
        salary_day=Decimal(salary_day),
    )


@pytest.mark.parametrize(
    "salary_day, other_salary_day, work_price, amount",
    [
        # Exact rounding-tie boundaries where the two paths diverged before
        # 3758fbf7 replaced round() with Decimal.quantize(ROUND_HALF_UP).
        (1, 31, "1000.00", "3"),
        (1, 159, "1000.00", "3"),
        (1, 799, "1000.00", "3"),
        (2, 62, "1000.00", "3"),
        (2, 318, "1000.00", "3"),
        (2, 1598, "1000.00", "3"),
        # a non-boundary, everyday case
        (5, 45, "250.50", "2"),
    ],
)
def test_creation_and_sync_paths_agree_on_amount_price(
    salary_day, other_salary_day, work_price, amount
):
    """
    Piecework.amount_price is computed by two independent code paths:
    - creation: calculate_salary_percentages + calculate_work_amount_price
    - sync (DailyWork.save() -> sync_piecework_with_dailywork):
      calculate_piecework_update
    They must keep agreeing, or editing a DailyWork silently changes the
    amount_price of an already-created Piecework record.
    """
    work = SimpleNamespace(price=Decimal(work_price))
    employee_salary = _salary(1, salary_day)
    employees_salary = [employee_salary, _salary(2, other_salary_day)]
    amount_decimal = Decimal(amount)

    percent = calculate_salary_percentages(employees_salary)[1]
    creation_price = calculate_work_amount_price(
        work_price=work.price, percent=percent, amount_decimal=amount_decimal
    )

    sync_price = calculate_piecework_update(
        work, amount_decimal, employee_salary, employees_salary
    )

    assert creation_price == sync_price
