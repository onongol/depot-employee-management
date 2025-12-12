def filter_month_year(queryset, month=None, year=None):
    """Reusable filter for DailySalary queryset."""
    if month:
        queryset = queryset.filter(salary_date__month=int(month))
    if year:
        queryset = queryset.filter(salary_date__year=int(year))
    return queryset
