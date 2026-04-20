from django.db.models import Q

from employee.constants.constants import DEFAULT_WAGON_NUMBER, DEFAULT_WAGON_TYPE
from employee.utils.converting_date import parse_date_range


def filter_pieceworks(queryset, context):
    """Reusable filter for Piecework queryset."""
    employee_id = context.employee_id
    employee_code = context.employee_code
    employee_name = context.employee_name
    job_title = context.job_title
    work_name = context.work_name
    type_work = context.type_work
    wagon_number = context.wagon_number
    type_wagon = context.type_wagon
    range_date = context.range_date
    record_date = context.record_date

    if employee_id:
        queryset = queryset.filter(employee_id=employee_id)
    if employee_code:
        queryset = queryset.filter(employee_code=employee_code)
    if employee_name:
        queryset = queryset.filter(employee_name__icontains=employee_name)
    if job_title:
        queryset = queryset.filter(job_title=job_title)
    if work_name:
        queryset = queryset.filter(work_name__icontains=work_name)
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
    if range_date:
        start_date, end_date = parse_date_range(range_date)
        if start_date:
            queryset = queryset.filter(work_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(work_date__lte=end_date)
    if record_date:
        queryset = queryset.filter(record_date__date=record_date)
    return queryset
