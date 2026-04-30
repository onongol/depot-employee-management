from django.core.cache import cache


def get_years_filter_values(
    queryset, date_field, cache_prefix, department=None, timeout=60 * 60
):
    """
    Returns a list of unique years (as strings) from the queryset by date_field with caching.
    :param queryset: base queryset (already filtered)
    :param date_field: name of the date field (e.g., 'work_date')
    :param cache_prefix: string prefix for the cache key
    :param department: (optional) department code for cache key uniqueness
    :param timeout: cache lifetime in seconds
    :return: list of years (strings)
    """
    key = f"{cache_prefix}_years"

    if department:
        key += f"_{department}"

    years = cache.get(key)

    if years is None:
        years = [str(d.year) for d in queryset.dates(date_field, "year", order="DESC")]
        cache.set(key, years, timeout)

    return years
