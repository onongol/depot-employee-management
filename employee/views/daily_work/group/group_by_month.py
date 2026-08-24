from django.db.models import F, Sum


def group_daily_works_by_month(qs, *, show_wagon: bool):
    """Group daily works by month with totals."""

    group_fields = ["work_name", "job_title", "type_work", "year", "month"]

    if show_wagon:
        group_fields.insert(3, "type_wagon")
        group_fields.insert(4, "wagon_number")

    return (
        qs.annotate(year=F("work_year"), month=F("work_month"))
        .values(*group_fields)
        .annotate(
            total_amount=Sum("amount"),
            total_time=Sum("amount_time"),
            total_price=Sum("amount_price"),
        )
    )
