import logging

from django.db import transaction
from django.utils.translation import gettext_lazy as _

from employee.models.daily_salary_models import DailySalary


def bulk_daily_salary_create(new_records, errors):
    try:
        with transaction.atomic():
            DailySalary.objects.bulk_create(new_records)
    except Exception:
        logging.exception("Bulk create DailySalary failed")
        errors.append(_("Error saving daily salary records."))
        return False
    return True
