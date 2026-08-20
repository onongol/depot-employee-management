import logging
from datetime import date

import pytest

from employee.utils.converting_date import format_date, parse_date_range

JANUARY_2024 = (date(2024, 1, 1), date(2024, 1, 31))


@pytest.mark.parametrize(
    "range_date",
    [
        # " to " is what flatpickr's range mode actually emits (default locale).
        "2024-01-01 to 2024-01-31",
        "2024-01-01 - 2024-01-31",
        # En dash and em dash are matched bare, so the spaces are optional.
        "2024-01-01 – 2024-01-31",
        "2024-01-01–2024-01-31",
        "2024-01-01 — 2024-01-31",
        "2024-01-01—2024-01-31",
    ],
)
def test_parse_date_range_accepts_every_supported_separator(range_date):
    assert parse_date_range(range_date) == JANUARY_2024


def test_parse_date_range_strips_surrounding_whitespace():
    assert parse_date_range("  2024-01-01 to 2024-01-31  ") == JANUARY_2024


def test_parse_date_range_treats_a_single_date_as_a_one_day_range():
    # Flatpickr leaves the input at a single date until the second click lands,
    # so a submit mid-selection has to mean "just that day", not "no filter".
    assert parse_date_range("2024-01-05") == (date(2024, 1, 5), date(2024, 1, 5))


def test_parse_date_range_accepts_unpadded_month_and_day():
    assert parse_date_range("2024-1-5 to 2024-1-9") == (
        date(2024, 1, 5),
        date(2024, 1, 9),
    )


def test_parse_date_range_returns_a_reversed_range_unchanged():
    # Nothing here orders start/end. A backwards range is not rejected, it just
    # makes the downstream __range filter match zero rows.
    assert parse_date_range("2024-01-31 to 2024-01-01") == (
        date(2024, 1, 31),
        date(2024, 1, 1),
    )


def test_parse_date_range_rejects_a_calendar_invalid_date(caplog):
    # Django's parse_date raises ValueError (rather than returning None) for a
    # well-shaped but non-existent date, so the broad except is load-bearing.
    with caplog.at_level(logging.WARNING, logger="employee.utils.converting_date"):
        result = parse_date_range("2024-02-30 to 2024-03-01")

    assert result == (None, None)
    assert "Invalid date range" in caplog.text


def test_parse_date_range_rejects_a_range_with_a_missing_half():
    assert parse_date_range("2024-01-01 to ") == (None, None)


@pytest.mark.parametrize("range_date", ["", "   ", None])
def test_parse_date_range_returns_none_for_blank_input(range_date):
    assert parse_date_range(range_date) == (None, None)


def test_parse_date_range_rejects_a_bare_hyphen_separator():
    # ISO dates are full of hyphens, so only " - " (spaced) can separate them.
    assert parse_date_range("2024-01-01-2024-01-31") == (None, None)


def test_parse_date_range_rejects_a_separator_without_spaces():
    assert parse_date_range("2024-01-01to2024-01-31") == (None, None)


def test_parse_date_range_rejects_the_textual_formats_format_date_accepts():
    # parse_date_range goes through django's parse_date (ISO only) while
    # format_date has its own strptime list — the two do not accept the same
    # strings, so a date the create form takes is not one the filter takes.
    assert format_date("January 1, 2024") == date(2024, 1, 1)
    assert parse_date_range("January 1, 2024 to January 31, 2024") == (None, None)


def test_parse_date_range_accepts_basic_iso_that_format_date_rejects():
    # The inconsistency runs the other way too: date.fromisoformat takes the
    # compact form, format_date's "%Y-%m-%d" does not.
    assert parse_date_range("20240101 to 20240131") == JANUARY_2024
    assert format_date("20240101") is None


@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2024-01-01", date(2024, 1, 1)),
        ("2024-1-1", date(2024, 1, 1)),
        ("January 1, 2024", date(2024, 1, 1)),
        ("Jan 1, 2024", date(2024, 1, 1)),
    ],
)
def test_format_date_parses_every_supported_format(date_str, expected):
    assert format_date(date_str) == expected


@pytest.mark.parametrize("date_str", ["", None])
def test_format_date_returns_none_for_blank_input(date_str):
    assert format_date(date_str) is None


@pytest.mark.parametrize("date_str", ["not a date", "2024-13-01", "01/01/2024"])
def test_format_date_returns_none_for_unparseable_input(date_str):
    assert format_date(date_str) is None


def test_format_date_raises_on_a_real_date_object():
    # Despite the docstring, format_date only takes strings: strptime raises
    # TypeError and the loop only catches ValueError. Callers such as
    # daily_salary_create_instance already work around this with isinstance().
    with pytest.raises(TypeError):
        format_date(date(2024, 1, 1))
