import pytest

from employee.utils.month_period import parse_month_period


def _request(rf, query_string=""):
    return rf.get(f"/piecework/?{query_string}")


@pytest.mark.parametrize(
    "query_string",
    [
        "month_period=2024-03",
        "month_period=2024-3",
        "month_period=%202024-03%20",
    ],
)
def test_parse_month_period_normalises_the_new_format(rf, query_string):
    assert parse_month_period(_request(rf, query_string)) == (3, 2024, "2024-03")


@pytest.mark.parametrize(
    ("query_string", "expected"),
    [
        ("month_period=1900-01", (1, 1900, "1900-01")),
        ("month_period=9999-12", (12, 9999, "9999-12")),
    ],
)
def test_parse_month_period_accepts_the_range_boundaries(rf, query_string, expected):
    assert parse_month_period(_request(rf, query_string)) == expected


@pytest.mark.parametrize(
    "query_string",
    [
        "month_period=2024-13",
        "month_period=2024-00",
        "month_period=1899-12",
        "month_period=10000-01",
        "month_period=2024",
        "month_period=2024-03-15",
        "",
    ],
)
def test_parse_month_period_returns_empty_for_invalid_input(rf, query_string):
    assert parse_month_period(_request(rf, query_string)) == (None, None, "")


def test_parse_month_period_prefers_the_new_format_over_the_legacy_pair(rf):
    request = _request(rf, "month_period=2024-03&legacy_month=7&legacy_year=2020")

    assert parse_month_period(request) == (3, 2024, "2024-03")


def test_parse_month_period_ignores_the_legacy_pair_when_the_new_param_is_garbage(rf):
    # The legacy branch is an else, not a fallback: a non-empty but unparseable
    # month_period shadows a perfectly valid legacy month/year pair.
    request = _request(rf, "month_period=zzz&legacy_month=7&legacy_year=2020")

    assert parse_month_period(request) == (None, None, "")


def test_parse_month_period_falls_back_to_the_legacy_pair(rf):
    request = _request(rf, "legacy_month=7&legacy_year=2020")

    assert parse_month_period(request) == (7, 2020, "2020-07")


def test_parse_month_period_normalises_the_legacy_pair(rf):
    request = _request(rf, "legacy_month=07&legacy_year=2020")

    assert parse_month_period(request) == (7, 2020, "2020-07")


@pytest.mark.parametrize(
    "query_string",
    [
        "legacy_month=-7&legacy_year=2020",
        "legacy_month=7.0&legacy_year=2020",
        "legacy_month=7",
        "legacy_year=2020",
        "legacy_month=13&legacy_year=2020",
    ],
)
def test_parse_month_period_returns_empty_for_an_unusable_legacy_pair(rf, query_string):
    assert parse_month_period(_request(rf, query_string)) == (None, None, "")


def test_parse_month_period_reads_custom_param_names(rf):
    request = rf.get("/piecework/?period=2024-03&month=7&year=2020")

    assert parse_month_period(request, param_name="period") == (3, 2024, "2024-03")
    assert parse_month_period(request, legacy_month="month", legacy_year="year") == (
        7,
        2020,
        "2020-07",
    )


def test_parse_month_period_takes_the_last_value_of_a_repeated_param(rf):
    # QueryDict.get semantics, worth pinning: a duplicated filter param in a
    # bookmarked URL silently resolves to the last one.
    request = _request(rf, "month_period=2024-03&month_period=2025-06")

    assert parse_month_period(request) == (6, 2025, "2025-06")


def test_parse_month_period_crashes_on_a_non_ascii_digit_in_the_legacy_pair(rf):
    # str.isdigit() is Unicode-aware but int() is not, and unlike the
    # month_period branch the legacy branch has no try/except. A request for
    # ?legacy_month=² is a 500, not an ignored filter.
    request = _request(rf, "legacy_month=%C2%B2&legacy_year=2020")

    with pytest.raises(ValueError, match="invalid literal for int"):
        parse_month_period(request)
