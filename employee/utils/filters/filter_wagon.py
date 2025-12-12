from employee.constants.constants import DEFAULT_WAGON_TYPE
from employee.utils.converting_date import parse_date_range


def filter_wagon(queryset, wagon_number=None, type_wagon=None, work_name=None, type_work=None, range_date=None):
    """Reusable filter for Wagon queryset."""
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
    if range_date:
        start_date, end_date = parse_date_range(range_date)
        if start_date:
            queryset = queryset.filter(work_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(work_date__lte=end_date)
    return queryset
