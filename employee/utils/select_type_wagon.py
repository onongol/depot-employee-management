from django.db.models import Q

from employee.constants.constants import DEFAULT_WAGON_TYPE, ALLOWED_WAGON_DEPARTMENTS

def get_type_wagon_filter_values(department, always_include_default=False):
    """
    Returns a list of type_wagon values for filtering dropdown.
    :param department: The department to filter by.
    :param always_include_default: If True, always include the default option.
    """
    if not department or department not in ALLOWED_WAGON_DEPARTMENTS:
        return []

    # Import here to avoid circular imports
    from employee.models import Work
    from employee.utils.select_department import expand_department

    # Expand department to include all related departments
    deps = expand_department(department) or [department]

    # Query for distinct type_wagon values in these departments    
    qs = Work.objects.filter(department__in=deps)

    # Check for empty values
    has_empty = qs.filter(Q(type_wagon__isnull=True) | Q(type_wagon='')).exists()

    # Get distinct type_wagon values
    distinct_vals = list(
        qs.exclude(type_wagon__isnull=True)
          .exclude(type_wagon='')
          .values_list('type_wagon', flat=True)
          .distinct()
          .order_by()
    )

    # Always include the default option if specified or if there are empty entries
    if always_include_default or has_empty:
        return [DEFAULT_WAGON_TYPE] + distinct_vals
    return distinct_vals
