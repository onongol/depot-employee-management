from dataclasses import MISSING, fields
from datetime import date
from decimal import Decimal

from employee.constants.constants import (
    DEFAULT_WAGON_NUMBER,
    DEFAULT_WAGON_TYPE,
    Department,
    JobTitle,
    TypeWork,
)
from employee.models import DailyWork, Employee, Piecework, Work
from employee.views.daily_work.daily_work_context import DailyWorkContext
from employee.views.daily_work.daily_work_export.format_data import (
    iter_rows as daily_work_rows,
)
from employee.views.employee_salary.employee_salary_context import EmployeeSalaryContext
from employee.views.employee_salary.employee_salary_export.format_data import (
    iter_rows as salary_rows,
)
from employee.views.material.material_export.format_data import (
    iter_rows as material_rows,
)
from employee.views.piecework.piecework_context import PieceworkContext
from employee.views.piecework.piecework_export.format_data import (
    iter_rows as piecework_rows,
)
from employee.views.wagon.wagon_context import WagonContext
from employee.views.wagon.wagon_export.format_data import iter_rows as wagon_rows

# The exports are fed either model instances (detail view) or dicts from a
# grouped .values() query, so every row builder is exercised both ways.
# No DB: iter_rows only reads attributes/keys off whatever it is handed.


def make_context(cls, **flags):
    """Build a context with only the grouping flags set.

    iter_rows reads nothing but those flags; the twenty-odd remaining fields are
    filter state, so fill the required ones with None rather than spell them out.
    """
    required = {
        f.name: None
        for f in fields(cls)
        if f.default is MISSING and f.default_factory is MISSING
    }
    return cls(**(required | flags))


def make_piecework(**overrides):
    fields_ = {
        "employee": Employee(
            employee_id=777,
            employee_name="Related name",
            department=Department.MECHANIC,
        ),
        "employee_code": 101,
        "employee_name": "Snapshot name",
        "department": Department.ZASVAR_1,
        "job_title": JobTitle.GAGNUURCHIN,
        "work": Work(work_name="Related work"),
        "work_name": "Snapshot work",
        "type_work": TypeWork.TYPE_84,
        "wagon_number": "12",
        "type_wagon": "Type A",
        "amount": Decimal("3.00"),
        "amount_time": Decimal("1.50"),
        "amount_price": Decimal("4500.00"),
        "work_date": date(2026, 3, 14),
    }
    return Piecework(**(fields_ | overrides))


# --- piecework export ------------------------------------------------------


def test_piecework_rows_number_from_one_and_read_the_snapshot_fields():
    pieceworks = [make_piecework(), make_piecework(employee_code=102)]

    rows = list(piecework_rows(pieceworks, make_context(PieceworkContext)))

    # Snapshot fields win over the related objects: an export must keep showing
    # what was recorded then, not what the employee/work is named now.
    assert rows[0] == [
        1,
        101,
        "Snapshot name",
        Department.ZASVAR_1,
        JobTitle.GAGNUURCHIN,
        "Snapshot work",
        TypeWork.TYPE_84,
        Decimal("3.00"),
        Decimal("1.50"),
        Decimal("4500.00"),
        date(2026, 3, 14),
    ]
    assert rows[1][0] == 2


def test_piecework_rows_fall_back_to_related_objects_when_the_snapshot_is_blank():
    piecework = make_piecework(
        employee_code=None,
        employee_name="",
        department="",
        work_name="",
    )

    [row] = piecework_rows([piecework], make_context(PieceworkContext))

    assert row[1] == 777
    assert row[2] == "Related name"
    assert row[3] == Department.MECHANIC
    assert row[5] == "Related work"


def test_piecework_rows_use_the_display_properties_for_wagon_columns_when_ungrouped():
    piecework = make_piecework(wagon_number=None, type_wagon=None)

    [row] = piecework_rows([piecework], make_context(PieceworkContext, show_wagon=True))

    assert row[7:9] == [DEFAULT_WAGON_NUMBER, DEFAULT_WAGON_TYPE]
    assert len(row) == 13


def test_piecework_rows_month_group_appends_totals_and_month_year():
    group = {
        "employee_code": 101,
        "employee_name": "Snapshot name",
        "department": Department.ZASVAR_1,
        "job_title": JobTitle.GAGNUURCHIN,
        "work_name": "Snapshot work",
        "type_work": TypeWork.TYPE_84,
        # A grouped queryset carries the raw columns; the *_display properties
        # exist only on model instances.
        "wagon_number": "12",
        "type_wagon": "Type A",
        "total_amount": Decimal("9.00"),
        "total_time": Decimal("4.50"),
        "total_price": Decimal("13500.00"),
        "month": 3,
        "year": 2026,
    }

    [row] = piecework_rows(
        [group], make_context(PieceworkContext, show_wagon=True, month_group=True)
    )

    assert row == [
        1,
        101,
        "Snapshot name",
        Department.ZASVAR_1,
        JobTitle.GAGNUURCHIN,
        "Snapshot work",
        TypeWork.TYPE_84,
        "12",
        "Type A",
        Decimal("9.00"),
        Decimal("4.50"),
        Decimal("13500.00"),
        3,
        2026,
    ]


def test_piecework_rows_year_group_appends_the_year_without_the_month():
    group = {
        "employee_code": 101,
        "total_amount": Decimal("9.00"),
        "total_time": Decimal("4.50"),
        "total_price": Decimal("13500.00"),
        "year": 2026,
    }

    [row] = piecework_rows([group], make_context(PieceworkContext, year_group=True))

    assert row[7:] == [Decimal("9.00"), Decimal("4.50"), Decimal("13500.00"), 2026]


def test_piecework_rows_default_missing_keys_to_blank_and_zero():
    # get_value never raises on a missing key, so a renamed .values() column
    # silently exports an empty cell instead of blowing up.
    [row] = piecework_rows([{}], make_context(PieceworkContext, year_group=True))

    assert row == [1, "", "", "", "", "", "", 0, 0, 0, ""]


# --- daily work export -----------------------------------------------------


def test_daily_work_rows_fall_back_to_the_work_name_and_use_display_wagon_columns():
    daily_work = DailyWork(
        work=Work(work_name="Related work"),
        work_name="",
        job_title=JobTitle.BUDAGCHIN,
        type_work=TypeWork.TYPE_29,
        wagon_number=None,
        type_wagon=None,
        amount=Decimal("2.00"),
        amount_time=Decimal("1.00"),
        amount_price=Decimal("3000.00"),
        work_date=date(2026, 3, 15),
    )

    [row] = daily_work_rows(
        [daily_work], make_context(DailyWorkContext, show_wagon=True)
    )

    assert row == [
        1,
        "Related work",
        JobTitle.BUDAGCHIN,
        TypeWork.TYPE_29,
        DEFAULT_WAGON_NUMBER,
        DEFAULT_WAGON_TYPE,
        Decimal("2.00"),
        Decimal("1.00"),
        Decimal("3000.00"),
        date(2026, 3, 15),
    ]


def test_daily_work_rows_month_group_uses_the_raw_wagon_keys_and_appends_month_year():
    group = {
        "work_name": "Snapshot work",
        "job_title": JobTitle.BUDAGCHIN,
        "type_work": TypeWork.TYPE_29,
        "wagon_number": "12",
        "type_wagon": "Type A",
        "total_amount": Decimal("6.00"),
        "total_time": Decimal("3.00"),
        "total_price": Decimal("9000.00"),
        "month": 3,
        "year": 2026,
    }

    [row] = daily_work_rows(
        [group], make_context(DailyWorkContext, show_wagon=True, month_group=True)
    )

    assert row == [
        1,
        "Snapshot work",
        JobTitle.BUDAGCHIN,
        TypeWork.TYPE_29,
        "12",
        "Type A",
        Decimal("6.00"),
        Decimal("3.00"),
        Decimal("9000.00"),
        3,
        2026,
    ]


def test_daily_work_rows_year_group_defaults_missing_keys_to_blank_and_zero():
    [row] = daily_work_rows([{}], make_context(DailyWorkContext, year_group=True))

    assert row == [1, "", "", "", 0, 0, 0, ""]


# --- wagon export ----------------------------------------------------------


def test_wagon_rows_detail_columns_carry_the_work_and_the_date():
    item = {
        "wagon_number": "12",
        "type_wagon": "Type A",
        "work__work_name": "Snapshot work",
        "type_work": TypeWork.TYPE_84,
        "amount": Decimal("3.00"),
        "total_time": Decimal("1.50"),
        "total_price": Decimal("4500.00"),
        "work_date": date(2026, 3, 14),
    }

    [row] = wagon_rows([item], make_context(WagonContext))

    assert row == [
        1,
        "12",
        "Type A",
        "Snapshot work",
        TypeWork.TYPE_84,
        Decimal("3.00"),
        Decimal("1.50"),
        Decimal("4500.00"),
        date(2026, 3, 14),
    ]


def test_wagon_rows_month_group_collapses_to_totals_plus_month_year():
    item = {
        "wagon_number": "12",
        "type_wagon": "Type A",
        "total_time": Decimal("4.50"),
        "total_price": Decimal("13500.00"),
        "month": 3,
        "year": 2026,
    }

    [row] = wagon_rows([item], make_context(WagonContext, month_group=True))

    assert row == [1, "12", "Type A", Decimal("4.50"), Decimal("13500.00"), 3, 2026]


def test_wagon_rows_default_missing_keys_to_blank_and_zero():
    [row] = wagon_rows([{}], make_context(WagonContext))

    assert row == [1, "", "", "", "", 0, 0, 0, ""]


# --- employee salary export ------------------------------------------------


def test_salary_rows_read_the_employee_object_and_the_group_totals():
    item = {
        "employee": Employee(
            employee_id=777,
            employee_name="Related name",
            department=Department.MECHANIC,
            job_title=JobTitle.ZASVARCHIN,
            rank=2,
        ),
        "total_piecework_time": Decimal("4.50"),
        "total_piecework_amount": Decimal("13500.00"),
        "month": 3,
        "year": 2026,
    }

    [row] = salary_rows([item], make_context(EmployeeSalaryContext))

    assert row == [
        1,
        777,
        "Related name",
        Department.MECHANIC,
        JobTitle.ZASVARCHIN,
        2,
        Decimal("4.50"),
        Decimal("13500.00"),
        3,
        2026,
    ]


def test_salary_rows_wagon_mode_falls_back_to_the_default_wagon_number():
    employee = Employee(
        employee_id=777,
        employee_name="Related name",
        department=Department.MECHANIC,
        job_title=JobTitle.ZASVARCHIN,
        rank=2,
    )
    # Rows with no wagon are real: piecework outside wagon work groups under one
    # placeholder bucket rather than an empty cell.
    items = [
        {"employee": employee, "wagon_number": "12"},
        {"employee": employee},
    ]

    rows = list(
        salary_rows(items, make_context(EmployeeSalaryContext, wagon_mode=True))
    )

    assert rows[0][6] == "12"
    assert rows[1][6] == DEFAULT_WAGON_NUMBER
    assert rows[1][7:] == [0, 0, "", ""]


# --- material export -------------------------------------------------------


def test_material_rows_columns_and_defaults():
    items = [
        {
            "work__type_material": "Steel",
            "work__work_name": "Snapshot work",
            "amount_material": Decimal("12.00"),
            "work_date": date(2026, 3, 14),
        },
        {
            "work__type_material": None,
            "work__work_name": None,
            "amount_material": None,
            "work_date": None,
        },
    ]

    rows = list(material_rows(items))

    assert rows == [
        [1, "Steel", "Snapshot work", Decimal("12.00"), date(2026, 3, 14)],
        [2, "", "", 0, ""],
    ]
