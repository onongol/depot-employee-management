import hashlib

from django.core.cache import cache

from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS, DEFAULT_WAGON_TYPE


def get_type_wagon_filter_values(
    department,
    source_model: str = "work",
    always_include_default: bool = False,
):
    """
    Build a distinct list of type_wagon values for a filter widget.

    Parameters:
        department (str):
            The base department code selected by the user (must be in ALLOWED_WAGON_DEPARTMENTS).
        source_model (str):
            'work'      -> pull current type_wagon values from Work (live reference data).
            'piecework' -> pull snapshot values from Piecework.type_wagon (historical state).
        always_include_default (bool):
            If True, always prepend DEFAULT_WAGON_TYPE (placeholder for NULL).
            If False, prepend it only when there are NULL entries in the underlying data.
    """
    # Fast exit if department is not provided or not allowed to have wagon filtering.
    if not department or department not in ALLOWED_WAGON_DEPARTMENTS:
        return []

    # Create a unique cache key based on the function parameters
    raw_key = f"{department}:{source_model}:{always_include_default}"
    cache_key = f"wagon_filter_{hashlib.md5(raw_key.encode()).hexdigest()}"

    # Try to get the result from cache
    result = cache.get(cache_key)
    if result is not None:
        return result

    # Dynamically choose the source model and the department lookup path.
    deps = [department]

    # Dynamically choose the source model and the department lookup path.
    # Snapshot (historical) source: use Piecework entries and follow employee -> department.
    # Default / live source: use Work reference data, department lives directly on Work.
    if source_model == "piecework":
        from employee.models import Piecework as Model

        dep_lookup = "department__in"
        field = "type_wagon"
    elif source_model == "daily_work":
        from employee.models import DailyWork as Model

        dep_lookup = "department__in"
        field = "type_wagon"
    else:
        from employee.models import Work as Model

        dep_lookup = "department__in"
        field = "type_wagon"

    # Base queryset filtered by department(s).
    qs = Model.objects.filter(**{dep_lookup: deps})

    # Collect non-NULL distinct values only; NULL is represented separately (placeholder).
    raw_values = list(qs.values_list(field, flat=True).distinct().order_by())

    has_null = None in raw_values

    values = sorted([v for v in raw_values if v is not None])

    # Prepend placeholder if forced or if NULL values actually exist.
    if always_include_default or has_null:
        result = [DEFAULT_WAGON_TYPE] + values
    else:
        result = values

    cache.set(cache_key, result, timeout=10 * 60)  # Cache for 10 minutes

    return result
