import hashlib

from django.core.cache import cache

from employee.constants.constants import DEFAULT_WAGON_TYPE
from employee.models import DailyWork, Piecework, Work
from employee.utils.wagon_department import is_wagon_department

SOURCE_MODELS = {"piecework": Piecework, "daily_work": DailyWork}


def get_type_wagon_filter_values(
    department,
    source_model: str = "work",
    *,
    always_include_default: bool = False,
):
    """Build a distinct list of type_wagon values for a filter widget."""
    if not is_wagon_department(department):
        return []

    # Create a unique cache key based on the function parameters
    raw_key = f"{department}:{source_model}:{always_include_default}"
    cache_key = f"wagon_filter_{hashlib.md5(raw_key.encode(), usedforsecurity=False).hexdigest()}"

    # Try to get the result from cache
    result = cache.get(cache_key)
    if result is not None:
        return result

    # Dynamically choose the source model based on the requested data source.
    model = SOURCE_MODELS.get(source_model, Work)

    # Base queryset filtered by department.
    qs = model.objects.filter(department=department)

    # Collect non-NULL distinct values only; NULL is represented separately (placeholder).
    raw_values = list(qs.values_list("type_wagon", flat=True).distinct().order_by())

    has_null = None in raw_values

    values = sorted([v for v in raw_values if v is not None])

    # Prepend placeholder if forced or if NULL values actually exist.
    if always_include_default or has_null:
        result = [DEFAULT_WAGON_TYPE, *values]
    else:
        result = values

    cache.set(cache_key, result, timeout=10 * 60)

    return result
