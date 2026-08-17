from decimal import Decimal

from employee.views.daily_work.daily_work_create.calculation.calculate_work_amount_price import (
    calculate_work_amount_price,
)


def test_calculate_work_amount_price_basic():
    result = calculate_work_amount_price(
        work_price=Decimal("1000.00"), percent=Decimal("3.13"), amount_decimal=Decimal("3")
    )

    assert result == Decimal("93.90")


def test_calculate_work_amount_price_rounds_half_up_at_each_stage():
    # value = 1.00 * 12.5 / 100 = 0.125 -> ties round up to 0.13, not down to
    # 0.12 (banker's rounding). Then 0.13 * 0.5 = 0.065 -> ties round up again
    # to 0.07, not 0.06. Both quantize() calls must use ROUND_HALF_UP for this
    # to hold.
    result = calculate_work_amount_price(
        work_price=Decimal("1.00"), percent=Decimal("12.5"), amount_decimal=Decimal("0.5")
    )

    assert result == Decimal("0.07")


def test_calculate_work_amount_price_zero_percent_is_zero():
    result = calculate_work_amount_price(
        work_price=Decimal("1000.00"), percent=Decimal("0"), amount_decimal=Decimal("5")
    )

    assert result == Decimal("0.00")
