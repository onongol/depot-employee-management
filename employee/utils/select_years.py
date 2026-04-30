import hashlib

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
    raw_key = f"{cache_prefix}_years"
    if department:
        raw_key += f"_{department}"

    cache_key = f"{cache_prefix}_{hashlib.md5(raw_key.encode()).hexdigest()}"

    years = cache.get(cache_key)

    if years is None:
        years = [str(d.year) for d in queryset.dates(date_field, "year", order="DESC")]
        cache.set(cache_key, years, timeout)

    return years
