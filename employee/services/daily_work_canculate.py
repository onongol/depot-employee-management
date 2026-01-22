from decimal import Decimal


def canculate_amount_time(work, amount: Decimal):
    quantity = amount or Decimal("0")
    std_time = Decimal(str(getattr(work, "standard_time", 0) or 0))

    amount_time = (std_time * quantity).quantize(Decimal("0.000000"))

    return amount_time


def canculate_amount_material(work, amount: Decimal):
    quantity = amount or Decimal("0")
    usage_material = Decimal(str(getattr(work, "usage_material", 0) or 0))

    amount_material = (usage_material * quantity).quantize(Decimal("0.0000"))

    return amount_material


def canculate_amount_price(work, amount: Decimal):
    quantity = amount or Decimal("0")
    price = Decimal(str(getattr(work, "price", 0) or 0))

    amount_price = (price * quantity).quantize(Decimal("0.00"))

    return amount_price
