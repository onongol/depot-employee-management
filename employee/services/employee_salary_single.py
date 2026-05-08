from decimal import ROUND_HALF_UP, Decimal

from django.db.models import Sum

TWO = Decimal("0.01")


def get_employee_total_salary_day(employee, month, year):
    """Calculate total salary for the employee for a given month and year."""
    total_salary_day = (
        employee.dailysalary_set.filter(salary_month=month, salary_year=year).aggregate(
            total=Sum("salary_day")
        )["total"]
        or 0
    )
    return Decimal(str(total_salary_day)).quantize(TWO, rounding=ROUND_HALF_UP)


def get_employee_total_piecework_amount(employee, month, year):
    """Calculate total piecework amount for the employee for a given month and year."""
    from employee.models import Piecework

    total_piecework_amount = (
        Piecework.objects.filter(
            employee=employee, work_month=month, work_year=year
        ).aggregate(total=Sum("amount_price"))["total"]
        or 0
    )
    return Decimal(str(total_piecework_amount)).quantize(TWO, rounding=ROUND_HALF_UP)


def get_employee_total_salary(employee, month, year):
    """Calculate total salary including piecework for the employee for a given month and year."""
    total_salary_day = get_employee_total_salary_day(employee, month, year)
    total_piecework_amount = get_employee_total_piecework_amount(employee, month, year)
    total_salary = total_salary_day + total_piecework_amount
    return Decimal(str(total_salary)).quantize(TWO, rounding=ROUND_HALF_UP)
