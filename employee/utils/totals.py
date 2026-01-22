from django.db.models import Sum

from employee.constants.constants import GROUP_MONTH, GROUP_YEAR
from employee.utils.filters import filter_month_year


def calc_totals(qs):
    """Return totals for raw (non-grouped) queryset."""
    return qs.aggregate(
        total_amount=Sum("amount"),
        total_time=Sum("amount_time"),
        total_price=Sum("amount_price"),
    )


def calc_totals_for_group(
    qs,
    *,
    group: str | None,
    month: int | None = None,
    year: int | None = None,
    selected_year: str | None = None,
    date_field: str = "work_date",
):
    """Totals matching the same month/year constraints as grouping."""
    totals_qs = qs

    if group == GROUP_MONTH and month and year:
        totals_qs = filter_month_year(
            totals_qs, month=month, year=year, date_field=date_field
        )
    elif group == GROUP_YEAR and selected_year:
        totals_qs = filter_month_year(
            totals_qs, year=selected_year, date_field=date_field
        )

    return calc_totals(totals_qs)
