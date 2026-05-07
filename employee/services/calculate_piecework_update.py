from decimal import ROUND_HALF_UP, Decimal


def calculate_piecework_update(work, amount, daily_salary, employees_salary):
    """
    Update calculation of the amount price for a piecework record
    Returns (amount_price)
    """
    # Calculate the total salary for all employees in the department for the given date
    TWO = Decimal("0.01")

    employees_money_sum = sum(emp.salary_day for emp in employees_salary)
    percent = Decimal("0")

    if employees_money_sum > 0 and daily_salary:
        percent = (daily_salary.salary_day / employees_money_sum * 100).quantize(
            TWO, rounding=ROUND_HALF_UP
        )

    value = (work.price * percent / 100).quantize(TWO, rounding=ROUND_HALF_UP)
    amount_price = (
        (value * amount).quantize(TWO, rounding=ROUND_HALF_UP)
        if amount is not None
        else Decimal("0")
    )
    return amount_price
