import hashlib
import json
from django.core.cache import cache

def get_distinct_values(
    model,
    field,
    department=None,
    department_field=None,
    only_with_salary=False,
    extra_filters=None,
):
    """
    Returns a queryset of distinct values for the specified field and department.
    :param model: Django model (Employee or Piecework)
    :param field: field name (str), e.g. 'job_title', 'type_work', 'work__type_material'
    :param department: department to filter by (optional)
    :param department_field: field name for department filter (str), e.g. 'department', 'work__department'
    :param only_with_salary: for Employee, filter only those with DailySalary (optional)
    :param extra_filters: dict of additional filters
    :return: QuerySet of distinct values or cached result
    """

    # Create a unique cache key based on the function parameters
    raw_key = f"{model._meta.model_name}_{field}_{department}_{only_with_salary}_{extra_filters}"
    cache_key = f"distinct_{hashlib.md5(raw_key.encode()).hexdigest()}"

    # Try to get the result from cache
    result = cache.get(cache_key)
    if result is not None:
        return result
    
    # If not cached, query the database
    qs = model.objects.all()

    if department and department_field:
        qs = qs.filter(**{department_field: department})
    if only_with_salary:
        qs = qs.filter(dailysalary__isnull=False)
    if extra_filters:
        qs = qs.filter(**extra_filters)

    # Get distinct values and cache the result
    result = list(qs.order_by(field).values_list(field, flat=True).distinct())
    
    # Remove empty values from the result
    result = [v for v in result if v]

    cache.set(cache_key, result, timeout=10 * 60)  # Cache for 10 minutes

    return result
