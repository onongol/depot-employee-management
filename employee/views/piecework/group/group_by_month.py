from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear


def group_pieceworks_by_month(qs, *, show_wagon: bool):
    """
    Group pieceworks by month with totals (values()-queryset).
    """
    qs = qs.annotate(
        year=ExtractYear("work_date"),
        month=ExtractMonth("work_date"),
    )

    group_fields = [
        "employee_code",
        "employee_name",
        "job_title",
        "work_name",
        "type_work",
        "year",
        "month",
    ]

    if show_wagon:
        # keep stable column order
        group_fields.insert(5, "type_wagon")
        group_fields.insert(6, "wagon_number")

    return qs.values(*group_fields).annotate(
        total_amount=Sum("amount"),
        total_time=Sum("amount_time"),
        total_price=Sum("amount_price"),
    )
