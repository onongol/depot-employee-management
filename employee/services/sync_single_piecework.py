from decimal import Decimal


def sync_single_piecework(piecework, dailywork, employees_salary):
    """Synchronize a single Piecework record with its related DailyWork and recalculate amount_price."""
    # Local imports to avoid circular import issues
    from employee.models import DailySalary
    from employee.services.calculate_piecework_update import calculate_piecework_update

    # Synchronize fields from DailyWork to Piecework
    piecework.type_work = dailywork.type_work
    piecework.wagon_number = dailywork.wagon_number
    piecework.type_wagon = dailywork.type_wagon
    piecework.job_title = dailywork.job_title
    piecework.amount = dailywork.amount
    piecework.work_date = dailywork.work_date

    # Calculate amount_time for Piecework
    std_time = dailywork.work.standard_time
    std_time_dec = Decimal(str(std_time or 0))
    amt = piecework.amount or Decimal("0.000000")
    piecework.amount_time = (std_time_dec * amt).quantize(Decimal("0.000000"))

    # Get the DailySalary for the Piecework's employee on the work_date
    daily_salary = DailySalary.objects.filter(
        employee=piecework.employee, salary_date=dailywork.work_date
    ).first()

    # Recalculate amount_price
    new_price = calculate_piecework_update(
        dailywork.work, piecework.amount, daily_salary, employees_salary
    )

    # Update amount_price if changed
    if piecework.amount_price != new_price:
        piecework.amount_price = new_price

    # Save the updated Piecework
    piecework.save(
        update_fields=[
            "type_work",
            "wagon_number",
            "type_wagon",
            "job_title",
            "amount",
            "amount_time",
            "amount_price",
            "work_date",
            "work_year",
            "work_month",
        ]
    )
