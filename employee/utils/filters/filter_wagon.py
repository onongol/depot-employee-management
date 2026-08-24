from employee.constants.constants import DEFAULT_WAGON_TYPE


def filter_wagon(queryset, context):
    """Reusable filter for Wagon queryset."""
    wagon_number = context.wagon_number
    type_wagon = context.type_wagon
    work_name = context.work_name
    type_work = context.type_work
    date_from = context.date_from
    date_to = context.date_to

    if wagon_number:
        queryset = queryset.filter(wagon_number=wagon_number)
    if type_wagon:
        if type_wagon == DEFAULT_WAGON_TYPE:
            queryset = queryset.filter(type_wagon__isnull=True)
        else:
            queryset = queryset.filter(type_wagon=type_wagon)
    if work_name:
        queryset = queryset.filter(work__work_name__icontains=work_name)
    if type_work:
        queryset = queryset.filter(type_work=type_work)
    if date_from:
        queryset = queryset.filter(work_date__gte=date_from)
    if date_to:
        queryset = queryset.filter(work_date__lte=date_to)
    return queryset
