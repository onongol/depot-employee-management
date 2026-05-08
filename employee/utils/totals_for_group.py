from employee.utils.filters import filter_month_year
from employee.utils.totals import calc_totals


def calc_totals_for_group(
    qs,
    context,
    date_field: str = "work_date",
    month_field: str | None = None,
    year_field: str | None = None,
):
    """Totals matching the same month/year constraints as grouping."""

    month_group = getattr(context, "month_group", False)
    year_group = getattr(context, "year_group", False)
    month = getattr(context, "month", None)
    year = getattr(context, "year", None)
    selected_year = getattr(context, "selected_year", None)

    if month_group and month and year:
        if month_field and year_field:
            qs = qs.filter(**{month_field: month, year_field: year})
        else:
            qs = filter_month_year(qs, month=month, year=year, date_field=date_field)
    elif year_group and selected_year:
        if year_field:
            qs = qs.filter(**{year_field: selected_year})
        else:
            qs = filter_month_year(qs, year=selected_year, date_field=date_field)

    return calc_totals(qs)
