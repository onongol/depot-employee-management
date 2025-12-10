from decimal import Decimal
from django.utils.translation import gettext_lazy as _

from employee.models import Work
from employee.models import DailyWork


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
            work_name=work_obj.work_name,
            department=work_obj.department,
            type_work=type_work,
            wagon_number=wagon_number,
            type_wagon=getattr(work_obj, 'type_wagon', None),
            amount=amount,
            work_date=work_date,
        )

        # Store the created DailyWork record for linking to Piecework
        daily_works[wid] = daily_work

    return daily_works, works_dict
