from datetime import date

import pytest

from employee.forms.filter_forms import (
    DailySalaryFilterForm,
    WorkDateFilterForm,
    WorkDateForm,
)

JANUARY_2024 = (date(2024, 1, 1), date(2024, 1, 31))


def _range(range_date):
    """The parsed bounds, or None when the box held something unusable."""
    return WorkDateFilterForm.parse({"range_date": range_date}).get("range_date")


@pytest.mark.parametrize(
    "range_date",
    [
        # " to " is what flatpickr's range mode actually emits (default locale).
        "2024-01-01 to 2024-01-31",
        "2024-01-01 - 2024-01-31",
        "2024-01-01 – 2024-01-31",
        "2024-01-01—2024-01-31",
    ],
)
def test_range_accepts_every_supported_separator(range_date):
    assert _range(range_date) == JANUARY_2024


def test_range_strips_surrounding_whitespace():
    assert _range("  2024-01-01 to 2024-01-31  ") == JANUARY_2024


def test_a_single_date_is_a_one_day_range():
    # Flatpickr leaves the input at a single date until the second click lands,
    # so a submit mid-selection has to mean "just that day", not "no filter".
    assert _range("2024-01-05") == (date(2024, 1, 5), date(2024, 1, 5))


def test_a_reversed_range_is_returned_unchanged():
    # Nothing here orders start/end. A backwards range is not rejected, it just
    # makes the downstream filter match zero rows.
    assert _range("2024-01-31 to 2024-01-01") == (date(2024, 1, 31), date(2024, 1, 1))


@pytest.mark.parametrize(
    "range_date",
    [
        "2024-02-30 to 2024-03-01",  # well-shaped but no such calendar day
        "2024-01-01 to ",  # half a range
        "no dates here",
        # ISO dates are full of hyphens, so only " - " (spaced) can separate
        # them; an unspaced one leaves a string with no readable halves.
        "2024-01-01-2024-01-31",
    ],
)
def test_an_unusable_range_is_dropped(range_date):
    # Dropped, not reported: a typo in the box means "this filter is not
    # applied", never "match nothing".
    assert _range(range_date) is None


@pytest.mark.parametrize("range_date", ["", "   "])
def test_a_blank_range_is_an_empty_pair(range_date):
    assert _range(range_date) == (None, None)


def test_range_and_single_date_accept_the_same_formats():
    # The filter box and the create form used to run different parsers, so a
    # date one of them took was not necessarily one the other took. One list now.
    assert _range("January 1, 2024 to January 31, 2024") == JANUARY_2024
    assert _range("20240101 to 20240131") == JANUARY_2024
    assert WorkDateForm.parse({"work_date": "January 1, 2024"}).get(
        "work_date"
    ) == date(2024, 1, 1)
    assert WorkDateForm.parse({"work_date": "20240101"}).get("work_date") == date(
        2024, 1, 1
    )


@pytest.mark.parametrize(
    ("date_str", "expected"),
    [
        ("2024-01-01", date(2024, 1, 1)),
        ("2024-1-1", date(2024, 1, 1)),
        ("January 1, 2024", date(2024, 1, 1)),
        ("Jan 1, 2024", date(2024, 1, 1)),
    ],
)
def test_a_single_date_parses_every_supported_format(date_str, expected):
    assert WorkDateForm.parse({"work_date": date_str}).get("work_date") == expected


@pytest.mark.parametrize("date_str", ["", "not a date", "2024-13-01", "22.08.2026"])
def test_an_unusable_single_date_is_dropped(date_str):
    assert WorkDateForm.parse({"work_date": date_str}).get("work_date") is None


def test_a_missing_field_is_absent_rather_than_raising():
    # The list pages hand the whole QueryDict over; fields the page has no box
    # for simply come back empty.
    assert DailySalaryFilterForm.parse({}) == {"salary_date": None, "record_date": None}


def test_a_real_date_object_passes_through():
    # The old helper raised TypeError on one, which callers worked around with
    # isinstance() checks.
    assert WorkDateForm.parse({"work_date": date(2024, 1, 1)}).get("work_date") == date(
        2024, 1, 1
    )
