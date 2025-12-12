import logging
from decimal import Decimal


def sync_piecework_with_dailywork(dailywork):
    """
    Synchronize related Piecework records after a DailyWork is saved.

    Purpose:
    - Propagate normalized fields from DailyWork (type_work, wagon_number, type_wagon,
      job_title, amount, work_date) to linked Piecework entries.
    - Recompute derived values (amount_time, amount_price) based on the updated work settings
      and current DailySalary context (per employee and department/date).
    - Keep Piecework data consistent with its source DailyWork for accurate reporting/exports.

    Notes:
    - Runs post-save; uses local imports to avoid circular dependencies.
    - Fails safe: logs exceptions without interrupting the primary DailyWork save.
    """
    try:
        # Local imports to avoid circular import issues
        from employee.models import DailySalary, Piecework
        from employee.views.piecework.piecework_calculation import piecework_calculate_update

        # Get department from the related Work
        department = getattr(dailywork.work, 'department', None)

        # Get all DailySalary entries for employees in the department on the work_date
        employees_salary = DailySalary.objects.filter(
            employee__department=department,
            salary_date=dailywork.work_date
        )

        # Find all Piecework entries linked to this DailyWork
        related_pieceworks = Piecework.objects.filter(daily_work=dailywork)

        for pw in related_pieceworks:
            # Synchronize fields from DailyWork to Piecework
            pw.type_work = dailywork.type_work
            pw.wagon_number = dailywork.wagon_number
            pw.type_wagon = dailywork.type_wagon
            pw.job_title = dailywork.job_title
            pw.amount = dailywork.amount
            pw.work_date = dailywork.work_date

            # Calculate amount_time for Piecework
            std_time = getattr(dailywork.work, 'standard_time', None)
            std_time_dec = Decimal(str(std_time or 0))
            amt = pw.amount or Decimal('0.000000')
            pw.amount_time = (std_time_dec * amt).quantize(Decimal('0.000000'))

            # Get the DailySalary for the Piecework's employee on the work_date
            daily_salary = DailySalary.objects.filter(
                employee=pw.employee,
                salary_date=dailywork.work_date
            ).first()

            # Recalculate amount_price    
            new_price = piecework_calculate_update(dailywork.work, pw.amount, daily_salary, employees_salary)

            # Update amount_price if changed    
            if pw.amount_price != new_price:
                pw.amount_price = new_price

            # Save the updated Piecework
            pw.save(update_fields=[
                'type_work', 
                'wagon_number', 
                'type_wagon',
                'job_title',
                'amount',
                'amount_time',
                'amount_price',
                'work_date', 
            ])

    except Exception as e:
        # Don't break primary save if update fails; log the problem
        logger = logging.getLogger(__name__)
        logger.exception("Failed updating related Piecework prices for DailyWork %s: %s", getattr(dailywork, 'pk', None), str(e))
