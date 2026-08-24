from django.db.models import Q

from employee.constants.constants import DEFAULT_WAGON_NUMBER, DEFAULT_WAGON_TYPE


def filter_pieceworks(queryset, context):
    """Reusable filter for Piecework queryset."""
    employee_code = context.employee_code
    employee_name = context.employee_name
    job_title = context.job_title
    work_name = context.work_name
    type_work = context.type_work
    wagon_number = context.wagon_number
    type_wagon = context.type_wagon
    date_from = context.date_from
    date_to = context.date_to
    record_date = context.record_date

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
    if date_from:
        queryset = queryset.filter(work_date__gte=date_from)
    if date_to:
        queryset = queryset.filter(work_date__lte=date_to)
    if record_date:
        queryset = queryset.filter(record_date__date=record_date)
    return queryset
