def filter_material(queryset, context):
    """Reusable filter for Material queryset with date range."""
    work_name = context.work_name
    type_material = context.type_material
    date_from = context.date_from
    date_to = context.date_to

    if work_name:
        queryset = queryset.filter(work__work_name__icontains=work_name)
    if type_material:
        queryset = queryset.filter(work__type_material__icontains=type_material)
    if date_from:
        queryset = queryset.filter(work_date__gte=date_from)
    if date_to:
        queryset = queryset.filter(work_date__lte=date_to)
    return queryset
