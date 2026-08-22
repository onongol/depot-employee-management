import logging

from django.db import transaction
from django.utils.translation import gettext_lazy as _

from employee.services.admin_log_entries import log_object_additions
from employee.views.daily_work.daily_work_create.calculation.calculate_piecework_records import (
    calculate_piecework_records,
)
from employee.views.daily_work.daily_work_create.daily_work_create_entries import (
    daily_work_create_entries,
)
from employee.views.daily_work.daily_work_create.piecework_create_bulk import (
    piecework_create_bulk,
)
from employee.views.daily_work.validators.validate_create import CreateValidator


def create_daily_work_piecework_records(request_data, user=None):
    """Process piecework creation based on the request data."""
    validator = CreateValidator(request_data)

    employees_salary, errors = validator.validate()

    # After validation the input data
    if errors:
        return None, None, errors

    # Use a transaction to ensure atomicity of the entire operation, including creating DailyWork and Piecework records, and logging admin actions
    try:
        with transaction.atomic():
            # Create Daily_Work
            daily_works, works_dict = daily_work_create_entries(request_data)

            # Calculate Piecework records
            pieceworks, errors = calculate_piecework_records(
                request_data,
                employees_salary=employees_salary,
                works_dict=works_dict,
            )

            if errors:
                transaction.set_rollback(True)
                return None, None, errors

            # Create mapping of employees from validated salary list to avoid per-row queries
            employees_map = {
                str(emp.employee.id): emp.employee for emp in employees_salary
            }

            # Create Piecework
            piecework_create_bulk(pieceworks, daily_works, works_dict, employees_map)

            # Log the creation of DailyWork records in the admin log if a user is provided
            if user is not None:
                created_daily_works = list(daily_works.values())
                transaction.on_commit(
                    lambda: log_object_additions(user, created_daily_works)
                )

            return pieceworks, works_dict, []
    except Exception as exc:
        logging.exception("Error creating daily work and piecework records")
        return (
            None,
            None,
            [_("Error creating piecework records: %(error)s.") % {"error": str(exc)}],
        )
