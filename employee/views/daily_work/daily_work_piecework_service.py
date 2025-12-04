import logging
from uuid import uuid4
from decimal import Decimal
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from employee.models import Piecework
from employee.models import Work
from employee.models import DailyWork
from employee.views.piecework.piecework_calculation import piecework_calculate_records
from .validators import validate_daily_salary, validate_required


def create_daily_work_entries(selected_work_ids, amounts, job_title, type_work, wagon_number, work_date):
    """Create DailyWork entries for the selected works."""
    # Store created DailyWork records for linking to Piecework
    daily_works = {}

    # Prefetch all selected works in a single query for efficient access
    works = Work.objects.filter(pk__in=selected_work_ids)

    # Create a dictionary of works keyed by their primary key as string
    works_dict = {str(work.pk): work for work in works}

    # Create DailyWork records for each selected work
    for wid, work_obj in works_dict.items():
        # Get the amount for this work, defaulting to 0.00 if not provided
        amount_str = amounts.get(wid)
        amount = Decimal(amount_str) if amount_str else Decimal('0.00')

        # Import DailyWork model here to avoid circular imports
        #from employee.models import DailyWork

        # Create the DailyWork record
        daily_work = DailyWork.objects.create(
            job_title=job_title or work_obj.job_title,
            work=work_obj,
            type_work=type_work,
            wagon_number=wagon_number,
            type_wagon=getattr(work_obj, 'type_wagon', None),
            amount=amount,
            work_date=work_date,
        )

        # Store the created DailyWork record for linking to Piecework
        daily_works[wid] = daily_work

    return daily_works, works_dict


def process_piecework(request_data):
    """Process piecework creation based on the request data."""
    # Extract relevant fields from the request data
    work_date = request_data['work_date']
    type_work = request_data['type_work']
    wagon_number = request_data['wagon_number']
    selected_employee_ids = request_data['selected_employee_ids']
    selected_work_ids = request_data['selected_work_ids']
    amounts = request_data['amounts']
    job_title = request_data.get('job_title')

    # Initialize error list
    errors = []

    # Validate daily salary for selected employees
    employees_salary, salary_errors = validate_daily_salary(selected_employee_ids, work_date)

    # Append any salary validation errors
    errors.extend(salary_errors)

    # Return early if there are any errors
    if errors:
        return None, None, errors

    # Create DailyWork entries
    daily_works, works_dict = create_daily_work_entries(
        selected_work_ids, amounts, job_title, type_work, wagon_number, work_date
    )

    # Validate required fields and amounts
    errors.extend(validate_required(selected_employee_ids, selected_work_ids, work_date, type_work, amounts, works_dict))

    if errors:
        return None, None, errors

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

    # Create Piecework records within a transaction
    try:
        with transaction.atomic():
            group_id = str(uuid4())
            for data in results:
                work_id = data['work_id']
                data['daily_work'] = daily_works.get(work_id)
                data['group_id'] = group_id
                Piecework.objects.create(**data)
    except Exception as e:
        logging.exception("Error creating daily work/piecework")
        errors.append(_("Error creating piecework records: %(error)s") % {'error': str(e)})

    return results, works_dict, errors