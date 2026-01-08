from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear


def group_daily_works_by_month(qs, *, show_wagon: bool):
    """
    Group daily works by month with totals.
    """
    group_fields = ['work_name', 'job_title', 'type_work', 'year', 'month']

    if show_wagon:
        # keep same order you already used
        group_fields.insert(3, 'type_wagon')
        group_fields.insert(4, 'wagon_number')

    return (
        qs.annotate(year=ExtractYear('work_date'), month=ExtractMonth('work_date'))
          .values(*group_fields)
          .annotate(
              total_amount=Sum('amount'),
              total_time=Sum('amount_time'),
              total_price=Sum('amount_price'),
          )
    )
