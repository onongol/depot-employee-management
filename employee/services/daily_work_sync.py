import logging

from employee.services.sync_single_piecework import sync_single_piecework

logger = logging.getLogger(__name__)


def sync_piecework_with_dailywork(dailywork):
    """Sync linked Piecework records after DailyWork is saved. Fails safe."""
    try:
        from employee.models import DailySalary, Piecework

        related_pieceworks = list(Piecework.objects.filter(daily_work=dailywork))

        employee_ids = [piecework.employee_id for piecework in related_pieceworks]
        employees_salary = list(
            DailySalary.objects.select_related("employee").filter(
                employee__department=dailywork.department,
                employee_id__in=employee_ids,
                salary_date=dailywork.work_date,
            )
        )

        # Create a mapping of employee_id to DailySalary for quick lookup in sync_single_piecework
        salary_map = {
            dailysalary.employee_id: dailysalary for dailysalary in employees_salary
        }

        for piecework in related_pieceworks:
            sync_single_piecework(piecework, dailywork, salary_map)

    except Exception as e:
        logger.exception(
            "Failed updating related Piecework prices for DailyWork %s: %s",
            getattr(dailywork, "pk", None),
            str(e),
        )
