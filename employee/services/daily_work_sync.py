import logging

from employee.services.sync_single_piecework import sync_single_piecework

logger = logging.getLogger(__name__)


def sync_piecework_with_dailywork(dailywork):
    """
    Synchronize related Piecework records after a DailyWork is saved.

    Purpose:
    - Propagate normalized fields from DailyWork (type_work, wagon_number, type_wagon,
      job_title, amount, work_date) to linked Piecework entries.
    - Recompute derived values (amount_time, amount_price) based on the updated work settings
      and current DailySalary context for employees linked to this DailyWork/date.
    - Keep Piecework data consistent with its source DailyWork for accurate reporting/exports.

    Notes:
    - Runs post-save; uses local imports to avoid circular dependencies.
    - Fails safe: logs exceptions without interrupting the primary DailyWork save.
    """
    try:
        # Local imports to avoid circular import issues
        from employee.models import DailySalary, Piecework

        # Find all Piecework entries linked to this DailyWork
        related_pieceworks = list(Piecework.objects.filter(daily_work=dailywork))

        employee_ids = [piecework.employee_id for piecework in related_pieceworks]
        employees_salary = list(
            DailySalary.objects.select_related("employee").filter(
                employee__department=dailywork.department,
                employee_id__in=employee_ids,
                salary_date=dailywork.work_date,
            )
        )

        for piecework in related_pieceworks:
            sync_single_piecework(piecework, dailywork, employees_salary)

    except Exception as e:
        logger.exception(
            "Failed updating related Piecework prices for DailyWork %s: %s",
            getattr(dailywork, "pk", None),
            str(e),
        )
