import hashlib

from django.core.cache import cache


def get_distinct_values(
    model,
    field,
    department=None,
    *,
    only_with_salary=False,
    extra_filters=None,
):
    """Returns a queryset of distinct values for the specified field and department."""
    extra_filters = tuple(sorted(extra_filters.items())) if extra_filters else None

    # Create a unique cache key based on the function parameters
    raw_key = f"{model._meta.model_name}:{field}:{department}:{only_with_salary}:{extra_filters}"
    cache_key = (
        f"distinct_{hashlib.md5(raw_key.encode(), usedforsecurity=False).hexdigest()}"
    )

    # Try to get the result from cache
    result = cache.get(cache_key)
    if result is not None:
        return result

    # If not cached, query the database
    qs = model.objects.all()

    if department:
        qs = qs.filter(department=department)
    if only_with_salary:
        qs = qs.filter(dailysalary__isnull=False)
    if extra_filters:
        qs = qs.filter(**extra_filters)

    # Get distinct values and cache the result
    result = list(qs.order_by(field).values_list(field, flat=True).distinct())

    # Remove empty values from the result
    result = [v for v in result if v]

    cache.set(cache_key, result, timeout=10 * 60)

    return result
