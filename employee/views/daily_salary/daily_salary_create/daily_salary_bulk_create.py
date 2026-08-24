import logging

from django.db import transaction
from django.utils.translation import gettext_lazy as _
from simple_history.utils import bulk_create_with_history

from employee.models.daily_salary_models import DailySalary


def bulk_daily_salary_create(new_records, errors, user=None):
    try:
        with transaction.atomic():
            bulk_create_with_history(new_records, DailySalary, default_user=user)
    except Exception:
        logging.exception("Bulk create failed")
        errors.append(_("Error saving records."))
        return False
    return True
