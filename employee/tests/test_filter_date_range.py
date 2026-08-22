from datetime import date
from types import SimpleNamespace

import pytest

from employee.models import DailyWork, Piecework
from employee.tests.factories import DailyWorkFactory, PieceworkFactory
from employee.utils.filters.filter_daily_works import filter_daily_works
from employee.utils.filters.filter_material import filter_material
from employee.utils.filters.filter_pieceworks import filter_pieceworks
from employee.utils.filters.filter_wagon import filter_wagon

# All four filters carry the same copy-pasted range_date block, so they get the
# same treatment. filter_wagon and filter_material also run over DailyWork.
RANGE_FILTERS = [
    pytest.param(filter_daily_works, DailyWorkFactory, DailyWork, id="daily_works"),
    pytest.param(filter_pieceworks, PieceworkFactory, Piecework, id="pieceworks"),
    pytest.param(filter_wagon, DailyWorkFactory, DailyWork, id="wagon"),
    pytest.param(filter_material, DailyWorkFactory, DailyWork, id="material"),
]

FIRST = date(2024, 3, 10)
MIDDLE = date(2024, 3, 15)
LAST = date(2024, 3, 20)


def _context(range_date):
    """Every attribute the four filters read, with only range_date set."""
    return SimpleNamespace(
        range_date=range_date,
        record_date=None,
        work_name=None,
        job_title=None,
        type_work=None,
        type_material=None,
        wagon_number=None,
        type_wagon=None,
        employee_id=None,
        employee_code=None,
        employee_name=None,
    )


@pytest.mark.django_db
@pytest.mark.parametrize(("filter_func", "factory", "model"), RANGE_FILTERS)
def test_range_bounds_are_inclusive(filter_func, factory, model):
    # A range picked as "10th to 20th" has to contain the 10th and the 20th.
    rows = [factory(work_date=day) for day in (FIRST, MIDDLE, LAST)]

    result = filter_func(model.objects.all(), _context("2024-03-10 to 2024-03-20"))

    assert set(result.values_list("pk", flat=True)) == {row.pk for row in rows}


@pytest.mark.django_db
@pytest.mark.parametrize(("filter_func", "factory", "model"), RANGE_FILTERS)
def test_rows_outside_the_range_are_excluded(filter_func, factory, model):
    inside = factory(work_date=MIDDLE)
    factory(work_date=date(2024, 3, 9))
    factory(work_date=date(2024, 3, 21))

    result = filter_func(model.objects.all(), _context("2024-03-10 to 2024-03-20"))

    assert set(result.values_list("pk", flat=True)) == {inside.pk}


@pytest.mark.django_db
@pytest.mark.parametrize(("filter_func", "factory", "model"), RANGE_FILTERS)
def test_an_unparsable_range_leaves_the_queryset_untouched(filter_func, factory, model):
    # parse_date_range returns (None, None) here, and both bounds are guarded
    # by `if start_date` / `if end_date`. That has to mean "no date filter",
    # never "match nothing" — a typo in the box must not silently empty the
    # table and read as "no such records".
    for day in (FIRST, MIDDLE, LAST):
        factory(work_date=day)

    result = filter_func(model.objects.all(), _context("no dates here"))

    assert result.count() == 3


@pytest.mark.django_db
@pytest.mark.parametrize(("filter_func", "factory", "model"), RANGE_FILTERS)
def test_an_empty_range_leaves_the_queryset_untouched(filter_func, factory, model):
    factory(work_date=MIDDLE)

    result = filter_func(model.objects.all(), _context(""))

    assert result.count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize(("filter_func", "factory", "model"), RANGE_FILTERS)
def test_a_single_date_narrows_to_that_one_day(filter_func, factory, model):
    # Flatpickr leaves one date in the box between the two clicks, so this is
    # a real thing users submit.
    wanted = factory(work_date=MIDDLE)
    factory(work_date=FIRST)
    factory(work_date=LAST)

    result = filter_func(model.objects.all(), _context("2024-03-15"))

    assert set(result.values_list("pk", flat=True)) == {wanted.pk}


@pytest.mark.django_db
@pytest.mark.parametrize(("filter_func", "factory", "model"), RANGE_FILTERS)
def test_a_reversed_range_matches_nothing(filter_func, factory, model):
    # parse_date_range hands back start/end unordered, so this becomes
    # work_date >= 20th AND work_date <= 10th. Nothing is wrong with the
    # filter; the guard would have to live in the parser or the form.
    for day in (FIRST, MIDDLE, LAST):
        factory(work_date=day)

    result = filter_func(model.objects.all(), _context("2024-03-20 to 2024-03-10"))

    assert result.count() == 0
