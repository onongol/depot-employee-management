from employee.utils.filters import filter_month_year
from employee.utils.totals import calc_totals


def calc_totals_for_group(
    qs,
    context,
    date_field: str = "work_date",
):
    """Totals matching the same month/year constraints as grouping."""
    month_group = context.month_group
    year_group = context.year_group
    month = context.month
    year = context.year
    selected_year = context.selected_year

    if month_group and month and year:
        qs = filter_month_year(qs, month=month, year=year, date_field=date_field)
    elif year_group and selected_year:
        qs = filter_month_year(qs, year=selected_year, date_field=date_field)

    return calc_totals(qs)
