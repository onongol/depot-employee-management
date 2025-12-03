def apply_ordering(queryset, order_by, direction, allowed_fields, default='-record_date'):
    """
    Applies ordering to a queryset based on the specified field and direction.
    :param queryset: QuerySet to be ordered
    :param order_by: field name to order by (str)
    :param direction: 'asc' or 'desc'
    :param allowed_fields: list of allowed fields for ordering
    :param default: default ordering field or list/tuple of fields
    :return: ordered QuerySet
    """
    if order_by in allowed_fields:
        sort_field = f"-{order_by}" if direction == 'desc' else order_by
        return queryset.order_by(sort_field)
    
    # Support default as string or iterable of fields
    if isinstance(default, (list, tuple)):
        return queryset.order_by(*default)
    
    return queryset.order_by(default)
