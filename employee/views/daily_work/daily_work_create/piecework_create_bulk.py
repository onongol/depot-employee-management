import logging
from uuid import uuid4

from django.db import transaction
from django.utils.translation import gettext_lazy as _

from employee.models import Piecework


def piecework_create_bulk(results, daily_works, works_dict, employees_map, errors):
    """Bulk create Piecework records within a transaction."""
    try:
        with transaction.atomic():
            group_id = str(uuid4())
            for data in results:
                work_id = data["work_id"]
                emp_id = data["employee_id"]

                data["daily_work"] = daily_works.get(work_id)
                data["group_id"] = group_id

                emp_obj = employees_map.get(str(emp_id))
                work_obj = works_dict.get(str(work_id))

                # Snapshot fields
                data["employee_name"] = getattr(emp_obj, "name", None)
                data["work_name"] = getattr(work_obj, "work_name", None)
                data["department"] = getattr(emp_obj, "department", None)

                Piecework.objects.create(**data)
    except Exception as e:
        logging.exception("Error creating daily work, piecework")
        errors.append(
            _("Error creating piecework records: %(error)s.") % {"error": str(e)}
        )
