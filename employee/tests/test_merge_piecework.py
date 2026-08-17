from collections import defaultdict
from decimal import Decimal

from employee.views.employee_salary.calculation.merge_piecework import merge_piecework


def test_merge_piecework_keys_rows_by_wagon_when_grouping_by_wagon():
    salary_data = defaultdict(dict)
    piecework_groups = [
        {
            "employee": 1,
            "work_year": 2026,
            "work_month": 3,
            "wagon_number": "12",
            "total_piecework_amount": Decimal("300.00"),
            "total_piecework_time": Decimal("2.5"),
        },
        {
            "employee": 1,
            "work_year": 2026,
            "work_month": 3,
            "wagon_number": "45",
            "total_piecework_amount": Decimal("100.00"),
            "total_piecework_time": Decimal("1.0"),
        },
    ]

    merge_piecework(salary_data, piecework_groups=piecework_groups, group_by_wagon=True)

    assert salary_data[(1, 2026, 3, "12")]["total_piecework_amount"] == Decimal(
        "300.00"
    )
    assert salary_data[(1, 2026, 3, "45")]["total_piecework_amount"] == Decimal(
        "100.00"
    )


def test_merge_piecework_ignores_wagon_and_defaults_missing_totals_when_not_grouping():
    # group_by_wagon=False must fold everything into the wagon=None bucket
    # even if the group carries a wagon_number, and missing total keys (e.g.
    # a group with no time recorded) must default to 0 rather than KeyError.
    salary_data = defaultdict(dict)
    piecework_groups = [
        {"employee": 1, "work_year": 2026, "work_month": 3, "wagon_number": "12"}
    ]

    merge_piecework(
        salary_data, piecework_groups=piecework_groups, group_by_wagon=False
    )

    key = (1, 2026, 3, None)
    assert key in salary_data
    assert salary_data[key]["total_piecework_amount"] == 0
    assert salary_data[key]["total_piecework_time"] == 0
