from django.db import transaction

from employee.models.daily_salary_models import DailySalary
from employee.services.admin_log_entries import log_object_additions
from employee.views.daily_salary.daily_salary_create.daily_salary_build_instances import (
    build_daily_salary_instances,
)
from employee.views.daily_salary.daily_salary_create.daily_salary_bulk_create import (
    bulk_daily_salary_create,
)
from employee.views.daily_salary.daily_salary_create.selectors import (
    select_employees_by_ids,
    select_existing_employee_ids,
)
from employee.views.daily_salary.validators import validate_daily_salary_required


def create_daily_salary_records(selected_ids, salary_date, hours_per_day, user=None):
    """
    Create daily salary records for multiple employees.
    Returns:
        employees_dict (dict): Mapping of employee_id to Employee object.
        errors (list): List of error messages (empty if no errors).
    """
    errors = validate_daily_salary_required(selected_ids, salary_date, hours_per_day)

    # After required fields validation: if there are errors, stop processing and return them
    if errors:
        return None, errors

    # Check for existing records to avoid duplicates
    existing_records = select_existing_employee_ids(
        employee_ids=selected_ids, salary_date=salary_date
    )

    # Map employee IDs to their Employee objects
    employees_dict = select_employees_by_ids(selected_ids)

    new_records = build_daily_salary_instances(
        selected_ids,
        employees_dict,
        existing_records,
        salary_date,
        hours_per_day,
        errors,
    )

    # After duplicate check and instance preparation: if there are errors, stop and return them before saving
    if errors:
        return None, errors

    if not bulk_daily_salary_create(new_records, errors, user=user):
        return None, errors

    if user is not None and new_records:
        created_employee_ids = [record.employee_id for record in new_records]
        created_records = list(
            DailySalary.objects.filter(
                employee_code__in=created_employee_ids,
                salary_date=salary_date,
            )
        )
        transaction.on_commit(lambda: log_object_additions(user, created_records))

    return employees_dict, []
