from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear

from employee.utils.filters import filter_month_year
from employee.utils.group_modes import is_month_group


def get_grouped_wagons(
    qs,
    *,
    group: str | None,
    month: int | None = None,
    year: int | None = None,
):
    """
    Used by wagon list views/exports to apply the same grouping + sorting rules in one place.
    We group first (this adds month/year annotations in GROUP_MONTH mode) and only then sort,
    so ordering by month/year works and the UI behaves consistently across endpoints.
    """
    month_group = is_month_group(group)

    if month_group:
        if month and year:
            qs = filter_month_year(qs, month=month, year=year, date_field="work_date")

        qs = qs.annotate(
            year=ExtractYear("work_date"),
            month=ExtractMonth("work_date"),
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
