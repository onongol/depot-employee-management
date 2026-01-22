import logging
from uuid import uuid4

from django.db import transaction
from django.utils.translation import gettext_lazy as _

from employee.models import Piecework
from employee.views.daily_work.daily_work_create.daily_work_piecework_create_entries import (
    create_daily_work_entries,
)
from employee.views.daily_work.validators import (
    validate_daily_salary,
    validate_duplicate,
    validate_required,
)
from employee.views.piecework.piecework_calculation import piecework_calculate_records


def process_piecework(request_data):
    """Process piecework creation based on the request data."""
    # Extract relevant fields from the request data
    work_date = request_data["work_date"]
    type_work = request_data["type_work"]
    wagon_number = request_data["wagon_number"]
    selected_employee_ids = request_data["selected_employee_ids"]
    selected_work_ids = request_data["selected_work_ids"]
    amounts = request_data["amounts"]
    job_title = request_data.get("job_title")

    errors = []

    # Validate daily salary for selected employees
    employees_salary, salary_errors = validate_daily_salary(
        selected_employee_ids, work_date
    )
    errors.extend(salary_errors)

    # Validate no duplicate piecework entries
    errors.extend(
        validate_duplicate(
            selected_employee_ids, selected_work_ids, work_date, type_work, wagon_number
        )
    )

    # Validate required fields and amounts
    errors.extend(
        validate_required(
            selected_employee_ids, selected_work_ids, work_date, type_work, amounts
        )
    )

    if errors:
        return None, None, errors

    # Create DailyWork entries
    daily_works, works_dict = create_daily_work_entries(
        selected_work_ids, amounts, job_title, type_work, wagon_number, work_date
    )

    # Calculate piecework records
    results, calc_errors = piecework_calculate_records(
        employees_salary=employees_salary,
        selected_work_ids=selected_work_ids,
        amounts=amounts,
        works_dict=works_dict,
        work_date=work_date,
        type_work=type_work,
        wagon_number=wagon_number,
    )
    errors.extend(calc_errors)
    if errors:
        return None, None, errors

    # Create mapping of employees from validated salary list to avoid per-row queries
    employees_map = {
        str(ds.employee.employee_id): ds.employee for ds in employees_salary
    }

    # Create Piecework records within a transaction
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
        logging.exception("Error creating daily work/piecework")
        errors.append(
            _("Error creating piecework records: %(error)s") % {"error": str(e)}
        )

    return results, works_dict, errors
