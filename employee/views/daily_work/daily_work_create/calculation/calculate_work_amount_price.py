from decimal import ROUND_HALF_UP, Decimal

TWO = Decimal("0.01")


def calculate_work_amount_price(work_price, percent, amount_decimal):
    value = (work_price * percent / 100).quantize(TWO, rounding=ROUND_HALF_UP)
    return (value * amount_decimal).quantize(TWO, rounding=ROUND_HALF_UP)
