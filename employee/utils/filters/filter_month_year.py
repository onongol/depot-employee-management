def filter_month_year(queryset, month=None, year=None, *, date_field: str = "salary_date"):
    """Reusable month/year filter for querysets with a date/datetime field."""
    if month:
        queryset = queryset.filter(**{f"{date_field}__month": int(month)})
    if year:
        queryset = queryset.filter(**{f"{date_field}__year": int(year)})
    return queryset
