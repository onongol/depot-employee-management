import logging
from decimal import Decimal

from employee.services import sync_single_piecework


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

        # Get department from the related Work
        department = getattr(dailywork.work, "department", None)

        # Get all DailySalary entries for employees in the department on the work_date
        employees_salary = DailySalary.objects.filter(
            employee__department=department, salary_date=dailywork.work_date
        )

        # Find all Piecework entries linked to this DailyWork
        related_pieceworks = Piecework.objects.filter(daily_work=dailywork)

        for piecework in related_pieceworks:
            sync_single_piecework(piecework, dailywork, employees_salary)

    except Exception as e:
        # Don't break primary save if update fails; log the problem
        logger = logging.getLogger(__name__)
        logger.exception(
            "Failed updating related Piecework prices for DailyWork %s: %s",
            getattr(dailywork, "pk", None),
            str(e),
        )
