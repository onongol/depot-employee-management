from employee.utils.converting_date import parse_date_range


def filter_material(queryset, context):
    """Reusable filter for Material queryset with date range."""
    work_name = context.work_name
    type_material = context.type_material
    range_date = context.range_date

    if work_name:
        queryset = queryset.filter(work__work_name__icontains=work_name)
    if type_material:
        queryset = queryset.filter(work__type_material__icontains=type_material)
    if range_date:
        start_date, end_date = parse_date_range(range_date)
        if start_date:
            queryset = queryset.filter(work_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(work_date__lte=end_date)
    return queryset
