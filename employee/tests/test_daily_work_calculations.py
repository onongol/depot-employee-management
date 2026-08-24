from decimal import Decimal
from types import SimpleNamespace

from employee.services.daily_work_calculations import (
    calculate_material_amount,
    calculate_price_amount,
    calculate_time_amount,
)


def test_calculate_time_amount_basic():
    work = SimpleNamespace(standard_time=Decimal("1.500000"))

    result = calculate_time_amount(work, Decimal("3"))

    assert result == Decimal("4.500000")


def test_calculate_time_amount_rounds_half_up_at_six_decimals():
    # 0.0000005 * 1 is an exact tie at the 6th decimal: ROUND_HALF_UP -> 0.000001,
    # banker's rounding would give 0.000000 since 0 is even.
    work = SimpleNamespace(standard_time=Decimal("0.0000005"))

    result = calculate_time_amount(work, Decimal("1"))

    assert result == Decimal("0.000001")


def test_calculate_material_amount_basic():
    work = SimpleNamespace(usage_material=Decimal("2.5000"))

    result = calculate_material_amount(work, Decimal("4"))

    assert result == Decimal("10.0000")


def test_calculate_material_amount_rounds_half_up_at_four_decimals():
    # 0.00005 * 1 is an exact tie at the 4th decimal: ROUND_HALF_UP -> 0.0001,
    # banker's rounding would give 0.0000 since 0 is even.
    work = SimpleNamespace(usage_material=Decimal("0.00005"))

    result = calculate_material_amount(work, Decimal("1"))

    assert result == Decimal("0.0001")


def test_calculate_price_amount_basic():
    work = SimpleNamespace(price=Decimal("1000.00"))

    result = calculate_price_amount(work, Decimal("3"))

    assert result == Decimal("3000.00")


def test_calculate_price_amount_rounds_half_up_at_two_decimals():
    # 0.005 * 1 is an exact tie at the 2nd decimal: ROUND_HALF_UP -> 0.01,
    # banker's rounding would give 0.00 since 0 is even.
    work = SimpleNamespace(price=Decimal("0.005"))

    result = calculate_price_amount(work, Decimal("1"))

    assert result == Decimal("0.01")


def test_calculate_price_amount_none_amount_defaults_to_zero():
    work = SimpleNamespace(price=Decimal("1000.00"))

    result = calculate_price_amount(work, None)

    assert result == Decimal("0.00")


def test_calculate_price_amount_none_field_defaults_to_zero():
    work = SimpleNamespace(price=None)

    result = calculate_price_amount(work, Decimal(5))

    assert result == Decimal("0.00")


def test_calculate_price_amount_zero_amount_is_zero():
    work = SimpleNamespace(price=Decimal("1000.00"))

    result = calculate_price_amount(work, Decimal(0))

    assert result == Decimal("0.00")


def test_calculate_price_amount_negative_amount_is_not_guarded():
    # amount only gets MinValueValidator(0.01) at the model field level, and
    # DailyWork.save()/Piecework.save() never call full_clean() before this
    # runs, so a negative amount reaches here unguarded. calculate_time_amount
    # and calculate_material_amount share the same unguarded helper, so this
    # case is representative of all three, not just price.
    work = SimpleNamespace(price=Decimal("1000.00"))

    result = calculate_price_amount(work, Decimal(-3))

    assert result == Decimal("-3000.00")
