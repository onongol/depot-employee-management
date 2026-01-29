def calculate_piecework_update(work, amount, daily_salary, employees_salary):
    """
    Update calculation of the amount price for a piecework record
    Returns (amount_price)
    """
    # Calculate the total salary for all employees in the department for the given date
    employees_money_sum = sum(emp.salary_day for emp in employees_salary)
    percent = 0

    # Calculate the percentage for the current employee if possible
    if employees_money_sum > 0 and daily_salary:
        percent = round((daily_salary.salary_day / employees_money_sum) * 100, 2)

    # Calculate the value based on work price and employee's percent
    value = round((work.price * percent) / 100, 2)

    # Final amount_price is value multiplied by the amount
    amount_price = round(value * amount, 2) if amount is not None else 0
    return amount_price
