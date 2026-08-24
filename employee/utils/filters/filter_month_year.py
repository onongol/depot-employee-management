import calendar
from datetime import date


def filter_month_year(
    queryset, month=None, year=None, *, date_field: str = "salary_date"
):
    """Reusable month/year filter for querysets with a date/datetime field.

    When both month and year are given uses a date range (>= start, <= end)
    so the DB engine can use a B-tree index on the date column instead of EXTRACT().
    """
    if month and year:
        m, y = int(month), int(year)
        start = date(y, m, 1)
        end = date(y, m, calendar.monthrange(y, m)[1])
        queryset = queryset.filter(
            **{f"{date_field}__gte": start, f"{date_field}__lte": end}
        )
    elif month:
        queryset = queryset.filter(**{f"{date_field}__month": int(month)})
    elif year:
        queryset = queryset.filter(**{f"{date_field}__year": int(year)})
    return queryset
