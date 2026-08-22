import hashlib

from django.core.cache import cache


def get_years_filter_values(
    queryset, date_field, cache_prefix, department=None, timeout=60 * 60
):
    """Returns a list of unique years (as strings) from the queryset by date_field with caching."""
    raw_key = f"{cache_prefix}:years:{department or 'all'}"

    cache_key = f"{cache_prefix}_{hashlib.md5(raw_key.encode(), usedforsecurity=False).hexdigest()}"

    years = cache.get(cache_key)

    if years is None:
        years = [str(d.year) for d in queryset.dates(date_field, "year", order="DESC")]
        cache.set(cache_key, years, timeout)

    return years
