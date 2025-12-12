from django.db.models import Q

from employee.constants.constants import (DEFAULT_WAGON_NUMBER,
                                          DEFAULT_WAGON_TYPE)
from employee.utils.converting_date import parse_date_range


def filter_pieceworks(queryset, employee_id=None, employee_name=None, job_title=None, work_name=None, type_work=None, wagon_number=None, type_wagon=None, type_material=None, range_date=None, record_date=None):
    """Reusable filter for Piecework queryset."""
    if employee_id:
        queryset = queryset.filter(employee__employee_id=employee_id)
    if employee_name:
        queryset = queryset.filter(employee__name__icontains=employee_name)
    if job_title:
        queryset = queryset.filter(job_title=job_title)   
    if work_name:
        queryset = queryset.filter(work__work_name__icontains=work_name)
    if type_work:
        queryset = queryset.filter(type_work=type_work)
    if wagon_number:
        if wagon_number == DEFAULT_WAGON_NUMBER:
            queryset = queryset.filter(Q(wagon_number__isnull=True))
        else:
            queryset = queryset.filter(wagon_number=wagon_number)
    if type_wagon:
        if type_wagon == DEFAULT_WAGON_TYPE:
            queryset = queryset.filter(type_wagon__isnull=True)
        else:
            queryset = queryset.filter(type_wagon=type_wagon)
    if type_material:
        queryset = queryset.filter(work__type_material=type_material)
    if range_date:
        start_date, end_date = parse_date_range(range_date)
        if start_date:
            queryset = queryset.filter(work_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(work_date__lte=end_date)
    if record_date:
        queryset = queryset.filter(record_date__date=record_date)
    return queryset
