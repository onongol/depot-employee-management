from datetime import date, timedelta
from types import SimpleNamespace

import pytest
from django.utils import timezone

from employee.constants.constants import (
    DEFAULT_WAGON_NUMBER,
    DEFAULT_WAGON_TYPE,
    JobTitle,
    TypeWagon,
    TypeWork,
)
from employee.models import DailySalary, DailyWork, Employee, Piecework, Work
from employee.tests.factories import (
    DailySalaryFactory,
    DailyWorkFactory,
    EmployeeFactory,
    PieceworkFactory,
    WorkFactory,
)
from employee.utils.filters.filter_daily_salaries import filter_daily_salaries
from employee.utils.filters.filter_daily_works import filter_daily_works
from employee.utils.filters.filter_employees import filter_employees
from employee.utils.filters.filter_material import filter_material
from employee.utils.filters.filter_pieceworks import filter_pieceworks
from employee.utils.filters.filter_wagon import filter_wagon
from employee.utils.filters.filter_works import filter_works

# Every guard in these filters is optional, so the failure mode is silence: a
# filter that stops narrowing returns more rows instead of raising. Each test
# therefore plants a row that must survive and one that must not.
# The date-range guard has its own file (test_filter_date_range.py).


def make_context(**overrides):
    """Every attribute the eight context filters read, unset by default."""
    context = dict.fromkeys(
        [
            "employee_id",
            "employee_code",
            "employee_name",
            "job_title",
            "work_name",
            "type_work",
            "type_material",
            "wagon_number",
            "type_wagon",
            "date_from",
            "date_to",
            "record_date",
            "salary_date",
        ]
    )
    return SimpleNamespace(**(context | overrides))


ALL_FILTERS = [
    pytest.param(filter_daily_works, DailyWorkFactory, DailyWork, id="daily_works"),
    pytest.param(filter_pieceworks, PieceworkFactory, Piecework, id="pieceworks"),
    pytest.param(filter_wagon, DailyWorkFactory, DailyWork, id="wagon"),
    pytest.param(filter_material, DailyWorkFactory, DailyWork, id="material"),
    pytest.param(filter_works, WorkFactory, Work, id="works"),
    pytest.param(filter_employees, EmployeeFactory, Employee, id="employees"),
    pytest.param(
        filter_daily_salaries, DailySalaryFactory, DailySalary, id="daily_salaries"
    ),
]

# DailyWork and Piecework carry the same columns and the same guard block.
WORK_RECORD_FILTERS = [
    pytest.param(filter_daily_works, DailyWorkFactory, DailyWork, id="daily_works"),
    pytest.param(filter_pieceworks, PieceworkFactory, Piecework, id="pieceworks"),
]

# Both models snapshot employee_code/employee_name and keep the FK alongside.
SNAPSHOT_FILTERS = [
    pytest.param(filter_pieceworks, PieceworkFactory, Piecework, id="pieceworks"),
    pytest.param(
        filter_daily_salaries, DailySalaryFactory, DailySalary, id="daily_salaries"
    ),
]

RECORD_DATE_FILTERS = [
    pytest.param(filter_daily_works, DailyWorkFactory, DailyWork, id="daily_works"),
    pytest.param(filter_pieceworks, PieceworkFactory, Piecework, id="pieceworks"),
    pytest.param(
        filter_daily_salaries, DailySalaryFactory, DailySalary, id="daily_salaries"
    ),
]


@pytest.mark.django_db
@pytest.mark.parametrize(("filter_func", "factory", "model"), ALL_FILTERS)
def test_an_empty_context_leaves_the_queryset_untouched(filter_func, factory, model):
    row = factory()

    assert list(filter_func(model.objects.all(), context=make_context())) == [row]


# --- daily work / piecework guards -----------------------------------------


@pytest.mark.django_db
@pytest.mark.parametrize(("filter_func", "factory", "model"), WORK_RECORD_FILTERS)
def test_job_title_narrows_to_that_exact_title(filter_func, factory, model):
    wanted = factory(job_title=JobTitle.GAGNUURCHIN.value)
    factory(job_title=JobTitle.BUDAGCHIN.value)

    context = make_context(job_title=JobTitle.GAGNUURCHIN.value)

    assert list(filter_func(model.objects.all(), context=context)) == [wanted]


@pytest.mark.django_db
@pytest.mark.parametrize(("filter_func", "factory", "model"), WORK_RECORD_FILTERS)
def test_work_name_matches_a_substring_of_the_snapshot(filter_func, factory, model):
    # work_name is snapshotted from the Work on save, so the row inherits it.
    wanted = factory(work=WorkFactory(work_name="Alpha welding"))
    factory(work=WorkFactory(work_name="Beta painting"))

    context = make_context(work_name="welding")

    assert list(filter_func(model.objects.all(), context=context)) == [wanted]


@pytest.mark.django_db
@pytest.mark.parametrize(("filter_func", "factory", "model"), WORK_RECORD_FILTERS)
def test_type_work_narrows_to_that_exact_type(filter_func, factory, model):
    wanted = factory(type_work=TypeWork.TYPE_29.value)
    factory(type_work=TypeWork.TYPE_84.value)

    context = make_context(type_work=TypeWork.TYPE_29.value)

    assert list(filter_func(model.objects.all(), context=context)) == [wanted]


@pytest.mark.django_db
@pytest.mark.parametrize(("filter_func", "factory", "model"), WORK_RECORD_FILTERS)
def test_a_wagon_number_narrows_to_that_exact_wagon(filter_func, factory, model):
    wanted = factory(wagon_number="12")
    factory(wagon_number="45")

    context = make_context(wagon_number="12")

    assert list(filter_func(model.objects.all(), context=context)) == [wanted]


@pytest.mark.django_db
@pytest.mark.parametrize(("filter_func", "factory", "model"), WORK_RECORD_FILTERS)
def test_the_wagon_placeholder_selects_the_rows_without_a_wagon(
    filter_func, factory, model
):
    # "-" is what the UI shows for a NULL wagon, so picking it has to mean
    # isnull rather than a literal match on the dash.
    wanted = factory(wagon_number="")
    factory(wagon_number="12")

    context = make_context(wagon_number=DEFAULT_WAGON_NUMBER)

    assert list(filter_func(model.objects.all(), context=context)) == [wanted]


@pytest.mark.django_db
@pytest.mark.parametrize(("filter_func", "factory", "model"), WORK_RECORD_FILTERS)
def test_a_wagon_type_narrows_to_that_exact_type(filter_func, factory, model):
    # type_wagon is always taken from the Work, never from the record itself.
    wanted = factory(work=WorkFactory(type_wagon=TypeWagon.CHINGELG.value))
    factory(work=WorkFactory(type_wagon=TypeWagon.DUMPCAR.value))

    context = make_context(type_wagon=TypeWagon.CHINGELG.value)

    assert list(filter_func(model.objects.all(), context=context)) == [wanted]


@pytest.mark.django_db
@pytest.mark.parametrize(("filter_func", "factory", "model"), WORK_RECORD_FILTERS)
def test_the_wagon_type_placeholder_selects_the_rows_without_a_type(
    filter_func, factory, model
):
    wanted = factory(work=WorkFactory(type_wagon=None))
    factory(work=WorkFactory(type_wagon=TypeWagon.CHINGELG.value))

    context = make_context(type_wagon=DEFAULT_WAGON_TYPE)

    assert list(filter_func(model.objects.all(), context=context)) == [wanted]


# --- employee guards --------------------------------------------------------


@pytest.mark.django_db
def test_an_employee_id_narrows_to_that_employee_code():
    # On Employee itself employee_id IS the human code, not a foreign key.
    wanted = EmployeeFactory(employee_id=1042)
    EmployeeFactory(employee_id=1043)

    context = make_context(employee_id=1042)

    assert list(filter_employees(Employee.objects.all(), context=context)) == [wanted]


@pytest.mark.django_db
def test_an_employee_name_matches_a_substring():
    wanted = EmployeeFactory(employee_name="Batbayar")
    EmployeeFactory(employee_name="Ganbold")

    context = make_context(employee_name="atbay")

    assert list(filter_employees(Employee.objects.all(), context=context)) == [wanted]


@pytest.mark.django_db
def test_an_employee_job_title_narrows_to_that_exact_title():
    wanted = EmployeeFactory(job_title=JobTitle.GAGNUURCHIN.value)
    EmployeeFactory(job_title=JobTitle.BUDAGCHIN.value)

    context = make_context(job_title=JobTitle.GAGNUURCHIN.value)

    assert list(filter_employees(Employee.objects.all(), context=context)) == [wanted]


# --- employee columns snapshotted onto a record -----------------------------


@pytest.mark.django_db
@pytest.mark.parametrize(("filter_func", "factory", "model"), SNAPSHOT_FILTERS)
def test_an_employee_code_narrows_to_that_employee(filter_func, factory, model):
    wanted = factory(employee=EmployeeFactory(employee_id=1042))
    factory(employee=EmployeeFactory(employee_id=1043))

    context = make_context(employee_code=1042)

    assert list(filter_func(model.objects.all(), context=context)) == [wanted]


@pytest.mark.django_db
@pytest.mark.parametrize(("filter_func", "factory", "model"), SNAPSHOT_FILTERS)
def test_an_employee_id_reads_the_foreign_key_not_the_code(filter_func, factory, model):
    # Trap worth pinning down: on these records employee_id is the FK column,
    # not the visible code that lives in employee_code. Here one number is both
    # - first's pk and second's code - and the guard picks by pk, i.e. another
    # person than a user would expect. No filter form submits it; only a
    # hand-built URL gets here.
    first = factory()
    second = factory(employee=EmployeeFactory(employee_id=first.employee.pk))

    context = make_context(employee_id=first.employee.pk)

    rows = list(filter_func(model.objects.all(), context=context))

    assert rows == [first]
    assert second.employee_code == first.employee.pk


@pytest.mark.django_db
@pytest.mark.parametrize(("filter_func", "factory", "model"), SNAPSHOT_FILTERS)
def test_an_employee_name_on_a_record_matches_a_substring(filter_func, factory, model):
    wanted = factory(employee=EmployeeFactory(employee_name="Batbayar"))
    factory(employee=EmployeeFactory(employee_name="Ganbold"))

    context = make_context(employee_name="atbay")

    assert list(filter_func(model.objects.all(), context=context)) == [wanted]


# --- daily salary guards ----------------------------------------------------


@pytest.mark.django_db
def test_a_daily_salary_job_title_narrows_to_that_exact_title():
    wanted = DailySalaryFactory(
        employee=EmployeeFactory(job_title=JobTitle.GAGNUURCHIN.value)
    )
    DailySalaryFactory(employee=EmployeeFactory(job_title=JobTitle.BUDAGCHIN.value))

    context = make_context(job_title=JobTitle.GAGNUURCHIN.value)

    assert list(filter_daily_salaries(DailySalary.objects.all(), context=context)) == [
        wanted
    ]


@pytest.mark.django_db
def test_a_salary_date_narrows_to_that_one_day():
    wanted = DailySalaryFactory(salary_date=date(2026, 3, 14))
    DailySalaryFactory(salary_date=date(2026, 3, 15))

    context = make_context(salary_date=date(2026, 3, 14))

    assert list(filter_daily_salaries(DailySalary.objects.all(), context=context)) == [
        wanted
    ]


# --- work guards ------------------------------------------------------------


@pytest.mark.django_db
def test_a_work_job_title_narrows_to_that_exact_title():
    wanted = WorkFactory(job_title=JobTitle.GAGNUURCHIN.value)
    WorkFactory(job_title=JobTitle.BUDAGCHIN.value)

    context = make_context(job_title=JobTitle.GAGNUURCHIN.value)

    assert list(filter_works(Work.objects.all(), context=context)) == [wanted]


@pytest.mark.django_db
def test_a_work_name_matches_a_substring():
    wanted = WorkFactory(work_name="Alpha welding")
    WorkFactory(work_name="Beta painting")

    context = make_context(work_name="welding")

    assert list(filter_works(Work.objects.all(), context=context)) == [wanted]


@pytest.mark.django_db
def test_a_work_wagon_type_narrows_to_that_exact_type():
    wanted = WorkFactory(type_wagon=TypeWagon.CHINGELG.value)
    WorkFactory(type_wagon=TypeWagon.DUMPCAR.value)

    context = make_context(type_wagon=TypeWagon.CHINGELG.value)

    assert list(filter_works(Work.objects.all(), context=context)) == [wanted]


@pytest.mark.django_db
def test_the_work_wagon_type_placeholder_selects_the_works_without_a_type():
    wanted = WorkFactory(type_wagon=None)
    WorkFactory(type_wagon=TypeWagon.CHINGELG.value)

    context = make_context(type_wagon=DEFAULT_WAGON_TYPE)

    assert list(filter_works(Work.objects.all(), context=context)) == [wanted]


# --- wagon guards -----------------------------------------------------------


@pytest.mark.django_db
def test_a_wagon_report_number_narrows_to_that_exact_wagon():
    # No placeholder branch here on purpose: wagon_prepare already drops the
    # rows without a wagon from the base queryset.
    wanted = DailyWorkFactory(wagon_number="12")
    DailyWorkFactory(wagon_number="45")

    context = make_context(wagon_number="12")

    assert list(filter_wagon(DailyWork.objects.all(), context=context)) == [wanted]


@pytest.mark.django_db
def test_a_wagon_report_type_narrows_to_that_exact_type():
    wanted = DailyWorkFactory(work=WorkFactory(type_wagon=TypeWagon.CHINGELG.value))
    DailyWorkFactory(work=WorkFactory(type_wagon=TypeWagon.DUMPCAR.value))

    context = make_context(type_wagon=TypeWagon.CHINGELG.value)

    assert list(filter_wagon(DailyWork.objects.all(), context=context)) == [wanted]


@pytest.mark.django_db
def test_the_wagon_report_type_placeholder_selects_the_rows_without_a_type():
    wanted = DailyWorkFactory(work=WorkFactory(type_wagon=None))
    DailyWorkFactory(work=WorkFactory(type_wagon=TypeWagon.CHINGELG.value))

    context = make_context(type_wagon=DEFAULT_WAGON_TYPE)

    assert list(filter_wagon(DailyWork.objects.all(), context=context)) == [wanted]


@pytest.mark.django_db
def test_a_wagon_report_work_name_matches_a_substring_of_the_related_work():
    wanted = DailyWorkFactory(work=WorkFactory(work_name="Alpha welding"))
    DailyWorkFactory(work=WorkFactory(work_name="Beta painting"))

    context = make_context(work_name="welding")

    assert list(filter_wagon(DailyWork.objects.all(), context=context)) == [wanted]


@pytest.mark.django_db
def test_a_wagon_report_type_work_narrows_to_that_exact_type():
    wanted = DailyWorkFactory(type_work=TypeWork.TYPE_29.value)
    DailyWorkFactory(type_work=TypeWork.TYPE_84.value)

    context = make_context(type_work=TypeWork.TYPE_29.value)

    assert list(filter_wagon(DailyWork.objects.all(), context=context)) == [wanted]


# --- material guards --------------------------------------------------------


@pytest.mark.django_db
def test_a_material_work_name_matches_a_substring_of_the_related_work():
    wanted = DailyWorkFactory(work=WorkFactory(work_name="Alpha welding"))
    DailyWorkFactory(work=WorkFactory(work_name="Beta painting"))

    context = make_context(work_name="welding")

    assert list(filter_material(DailyWork.objects.all(), context=context)) == [wanted]


@pytest.mark.django_db
def test_a_material_type_matches_a_substring_of_the_related_work():
    wanted = DailyWorkFactory(work=WorkFactory(type_material="Steel sheet"))
    DailyWorkFactory(work=WorkFactory(type_material="Copper wire"))

    context = make_context(type_material="steel")

    assert list(filter_material(DailyWork.objects.all(), context=context)) == [wanted]


# --- record date ------------------------------------------------------------


@pytest.mark.django_db
@pytest.mark.parametrize(("filter_func", "factory", "model"), RECORD_DATE_FILTERS)
def test_a_record_date_narrows_to_the_rows_entered_that_day(
    filter_func, factory, model
):
    # record_date is auto_now_add, so the older row has to be backdated after
    # the fact. On MySQL this lookup goes through CONVERT_TZ - if the server
    # ever loses its timezone tables the filter returns nothing instead of
    # failing, and this test is what catches it.
    fresh = factory()
    stale = factory()
    model.objects.filter(pk=stale.pk).update(
        record_date=timezone.now() - timedelta(days=2)
    )

    context = make_context(record_date=timezone.localdate())

    assert list(filter_func(model.objects.all(), context=context)) == [fresh]
