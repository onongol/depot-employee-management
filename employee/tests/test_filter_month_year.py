from datetime import date, timedelta
from types import SimpleNamespace

import pytest

from employee.models import DailySalary, DailyWork
from employee.tests.factories import DailySalaryFactory, DailyWorkFactory
from employee.utils.filters import filter_month_year
from employee.utils.totals import calc_totals
from employee.utils.totals_for_group import calc_totals_for_group

# Last days are hardcoded rather than computed: deriving them with
# calendar.monthrange here would just re-run the code under test.
BOUNDARY_MONTHS = [
    pytest.param(2024, 2, 29, id="february-leap"),
    pytest.param(2023, 2, 28, id="february-common"),
    pytest.param(2024, 1, 31, id="january"),
    pytest.param(2024, 4, 30, id="thirty-day-month"),
    pytest.param(2024, 12, 31, id="december"),
]


def _edges(year, month, last_day):
    """The four dates that matter: just outside and exactly on each edge."""
    first = date(year, month, 1)
    last = date(year, month, last_day)
    return first - timedelta(days=1), first, last, last + timedelta(days=1)


@pytest.mark.django_db
@pytest.mark.parametrize(("year", "month", "last_day"), BOUNDARY_MONTHS)
def test_filter_month_year_includes_both_edges_of_the_month(year, month, last_day):
    before, first, last, after = _edges(year, month, last_day)
    inside = [DailyWorkFactory(work_date=first), DailyWorkFactory(work_date=last)]
    DailyWorkFactory(work_date=before)
    DailyWorkFactory(work_date=after)

    result = filter_month_year(
        DailyWork.objects.all(), month=month, year=year, date_field="work_date"
    )

    assert set(result.values_list("pk", flat=True)) == {row.pk for row in inside}


@pytest.mark.django_db
def test_filter_month_year_uses_salary_date_by_default():
    DailySalaryFactory(salary_date=date(2024, 3, 31))
    outside = DailySalaryFactory(salary_date=date(2024, 4, 1))

    result = filter_month_year(DailySalary.objects.all(), month=3, year=2024)

    assert result.count() == 1
    assert outside.pk not in set(result.values_list("pk", flat=True))


@pytest.mark.django_db
def test_filter_month_year_with_only_month_matches_that_month_in_every_year():
    same_month_other_year = DailyWorkFactory(work_date=date(2023, 2, 10))
    this_month = DailyWorkFactory(work_date=date(2024, 2, 10))
    DailyWorkFactory(work_date=date(2024, 3, 10))

    result = filter_month_year(DailyWork.objects.all(), month=2, date_field="work_date")

    assert set(result.values_list("pk", flat=True)) == {
        same_month_other_year.pk,
        this_month.pk,
    }


@pytest.mark.django_db
def test_filter_month_year_with_only_year_matches_every_month_of_that_year():
    january = DailyWorkFactory(work_date=date(2024, 1, 1))
    december = DailyWorkFactory(work_date=date(2024, 12, 31))
    DailyWorkFactory(work_date=date(2025, 1, 1))

    result = filter_month_year(
        DailyWork.objects.all(), year=2024, date_field="work_date"
    )

    assert set(result.values_list("pk", flat=True)) == {january.pk, december.pk}


@pytest.mark.django_db
def test_filter_month_year_without_month_or_year_returns_everything():
    DailyWorkFactory(work_date=date(2024, 2, 10))
    DailyWorkFactory(work_date=date(2025, 7, 20))

    result = filter_month_year(DailyWork.objects.all(), date_field="work_date")

    assert result.count() == 2


@pytest.mark.django_db
@pytest.mark.parametrize(("year", "month", "last_day"), BOUNDARY_MONTHS)
def test_date_range_and_denormalised_column_paths_select_the_same_rows(
    year, month, last_day
):
    """The month/year window is computed two independent ways.

    filter_month_year() builds a date range off work_date, while the grouped
    list and calc_totals_for_group() filter on the denormalised work_month /
    work_year columns that DailyWork.save() derives from that same date. If the
    two ever drift apart, the totals row stops matching the rows above it.
    """
    for work_date in _edges(year, month, last_day):
        DailyWorkFactory(work_date=work_date)

    by_date_range = filter_month_year(
        DailyWork.objects.all(), month=month, year=year, date_field="work_date"
    )
    by_columns = DailyWork.objects.filter(work_month=month, work_year=year)

    assert set(by_date_range.values_list("pk", flat=True)) == set(
        by_columns.values_list("pk", flat=True)
    )
    assert calc_totals(by_date_range) == calc_totals(by_columns)


@pytest.mark.django_db
@pytest.mark.parametrize(("year", "month", "last_day"), BOUNDARY_MONTHS)
def test_calc_totals_for_group_agrees_with_and_without_denormalised_fields(
    year, month, last_day
):
    # Both branches of calc_totals_for_group must produce the same totals; only
    # the query plan is supposed to differ.
    for work_date in _edges(year, month, last_day):
        DailyWorkFactory(work_date=work_date)
    context = SimpleNamespace(
        month_group=True, year_group=False, month=month, year=year, selected_year=None
    )

    with_columns = calc_totals_for_group(
        DailyWork.objects.all(),
        context,
        date_field="work_date",
        month_field="work_month",
        year_field="work_year",
    )
    with_date_range = calc_totals_for_group(
        DailyWork.objects.all(), context, date_field="work_date"
    )

    assert with_columns == with_date_range


@pytest.mark.django_db
def test_calc_totals_for_group_year_branch_agrees_with_and_without_year_field():
    DailyWorkFactory(work_date=date(2024, 1, 1))
    DailyWorkFactory(work_date=date(2024, 12, 31))
    DailyWorkFactory(work_date=date(2025, 1, 1))
    context = SimpleNamespace(
        month_group=False, year_group=True, month=None, year=None, selected_year=2024
    )

    with_column = calc_totals_for_group(
        DailyWork.objects.all(),
        context,
        date_field="work_date",
        year_field="work_year",
    )
    with_date_range = calc_totals_for_group(
        DailyWork.objects.all(), context, date_field="work_date"
    )

    assert with_column == with_date_range
