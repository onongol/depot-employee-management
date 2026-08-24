from decimal import Decimal

from employee.views.daily_work.validators.validate_parse_amount import (
    validate_parse_amount,
)


def test_validate_parse_amount_returns_decimal_for_valid_amount():
    errors = []

    result = validate_parse_amount("3.5", "Lathe", errors)

    assert result == Decimal("3.5")
    assert errors == []


def test_validate_parse_amount_appends_required_error_for_empty_or_none():
    for amount in ("", None):
        errors = []

        result = validate_parse_amount(amount, "Lathe", errors)

        assert result is None
        assert len(errors) == 1
        assert "required" in str(errors[0])


def test_validate_parse_amount_appends_invalid_error_for_non_numeric_string():
    errors = []

    result = validate_parse_amount("abc", "Lathe", errors)

    assert result is None
    assert len(errors) == 1
    assert "Invalid" in str(errors[0])


def test_validate_parse_amount_negative_number_is_not_guarded():
    # "-5" is truthy as a string and parses cleanly as a Decimal, so nothing
    # here rejects a negative amount — same gap as calculate_time_amount etc.
    errors = []

    result = validate_parse_amount("-5", "Lathe", errors)

    assert result == Decimal("-5")
    assert errors == []
