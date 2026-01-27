from employee.constants.constants import DEFAULT_WAGON_TYPE


def filter_works(queryset, context):
    """Reusable filter for Work queryset."""
    department = context.selected_department
    job_title = context.job_title
    work_name = context.work_name
    type_wagon = context.type_wagon

    if department:
        queryset = queryset.filter(department=department)
    if job_title:
        queryset = queryset.filter(job_title=job_title)
    if work_name:
        queryset = queryset.filter(work_name__icontains=work_name)
    if type_wagon:
        if type_wagon == DEFAULT_WAGON_TYPE:
            queryset = queryset.filter(type_wagon__isnull=True)
        else:
            queryset = queryset.filter(type_wagon=type_wagon)
    return queryset
