from decimal import ROUND_HALF_UP, Decimal

_PRECISION_TIME = Decimal("0.000000")
_PRECISION_MATERIAL = Decimal("0.0000")
_PRECISION_PRICE = Decimal("0.00")


def _work_field_multiply(field_value, amount: Decimal, precision: Decimal) -> Decimal:
    quantity = amount or Decimal("0")
    value = Decimal(str(field_value or 0))
    return (value * quantity).quantize(precision, rounding=ROUND_HALF_UP)


def calculate_time_amount(work, amount: Decimal) -> Decimal:
    return _work_field_multiply(work.standard_time, amount, _PRECISION_TIME)


def calculate_material_amount(work, amount: Decimal) -> Decimal:
    return _work_field_multiply(work.usage_material, amount, _PRECISION_MATERIAL)


def calculate_price_amount(work, amount: Decimal) -> Decimal:
    return _work_field_multiply(work.price, amount, _PRECISION_PRICE)
