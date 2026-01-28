def calculate_amount_price(work_price, percent, amount_decimal):
    value = round((work_price * percent) / 100, 2)
    return round(value * amount_decimal, 2)
