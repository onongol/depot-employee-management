import logging
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from employee.models import Employee, DailySalary
from .validators import validate_required_daily_salary


def create_daily_salary_records(selected_ids, salary_date, hours_per_day):
    """Create daily salary records for multiple employees."""
    # Validate required fields
    errors = validate_required_daily_salary(selected_ids, salary_date, hours_per_day)

    if errors:
        return None, errors

    # Check for existing records to avoid duplicates
    existing_records = set(DailySalary.objects.filter(
        employee_id__in=selected_ids,
        salary_date=salary_date
    ).values_list('employee_id', flat=True))

    # Map employee IDs to their Employee objects
    employees_dict = {e.employee_id: e for e in Employee.objects.filter(employee_id__in=selected_ids)}

    # Check for duplicates and prepare new records
    new_records = []
    for emp_id in selected_ids:
        emp = employees_dict.get(emp_id)    # Get Employee object for the current employee ID
        if emp_id in existing_records:
            errors.append(
                _("Daily salary record for Employee: %(employee)s on %(date)s already exists!") % {
                    'employee': f"{emp_id}/{emp.name}",
                    'date': salary_date
                }
            )
        else:
            # Calculate salary_day manually
            salary_day = float(hours_per_day) * float(emp.money_per_hour)

            # Create new DailySalary instance
            new_records.append(
                DailySalary(
                    employee_id=emp_id,
                    salary_date=salary_date,
                    hours_per_day=hours_per_day,
                    salary_day=salary_day
                )
            )

    if errors:
        return None, errors

    # Bulk create new DailySalary records
    try:
        with transaction.atomic():
            DailySalary.objects.bulk_create(new_records)
    except Exception as exc:
        logging.exception("Bulk create DailySalary failed")
        errors.append(_("Error saving daily salary records."))
        return None, errors

    return {'employees_dict': employees_dict}, []
