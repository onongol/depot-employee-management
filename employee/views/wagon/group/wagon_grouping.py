from django.db.models import F, Sum


def get_grouped_wagons(
    qs,
    *,
    month_group: bool | None = None,
    month: int | None = None,
    year: int | None = None,
):
    """
    Used by wagon list views/exports to apply the same grouping + sorting rules in one place.
    We group first (this adds month/year annotations in GROUP_MONTH mode) and only then sort,
    so ordering by month/year works and the UI behaves consistently across endpoints.
    """
    if month_group:
        if month and year:
            qs = qs.filter(work_month=month, work_year=year)

        qs = qs.annotate(
            year=F("work_year"),
            month=F("work_month"),
        )

        return (
            qs.values("year", "month", "wagon_number", "type_wagon")
            .annotate(
                amount=Sum("amount"),
                total_time=Sum("amount_time"),
                total_price=Sum("amount_price"),
            )
            .order_by("-year", "-month", "wagon_number", "type_wagon")
        )

    return (
        qs.values(
            "work__work_name", "type_work", "wagon_number", "type_wagon", "work_date"
        )
        .annotate(
            amount=Sum("amount"),
            total_time=Sum("amount_time"),
            total_price=Sum("amount_price"),
        )
        .order_by(
            "-work_date", "work__work_name", "type_work", "wagon_number", "type_wagon"
        )
    )
