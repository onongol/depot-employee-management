from decimal import Decimal

from employee.models import DailyWork, Work


def daily_work_create_entries(
    selected_work_ids, amounts, job_title, type_work, wagon_number, work_date
):
    """Create DailyWork entries for the selected works."""
    # Store created DailyWork records for linking to Piecework
    daily_works = {}

    # Prefetch all selected works in a single query for efficient access
    works = Work.objects.filter(pk__in=selected_work_ids)

    # Create a dictionary of works keyed by their primary key as string
    works_dict = {str(work.pk): work for work in works}

    # For each selected work, create a DailyWork record with the provided details and store it for later linking to Piecework
    for work_id, work_obj in works_dict.items():
        amount_str = amounts.get(work_id)
        amount = Decimal(amount_str) if amount_str else Decimal("0.00")

        daily_work = DailyWork.objects.create(
            job_title=job_title or work_obj.job_title,
            work=work_obj,
            work_name=work_obj.work_name,
            department=work_obj.department,
            type_work=type_work,
            wagon_number=wagon_number,
            type_wagon=getattr(work_obj, "type_wagon", None),
            amount=amount,
            work_date=work_date,
        )

        daily_works[work_id] = daily_work

    return daily_works, works_dict
