from employee.constants.constants import DEFAULT_WAGON_TYPE


def filter_works(queryset, department=None, job_title=None, work_name=None, type_wagon=None):
    """Reusable filter for Work queryset."""
    if department:
        queryset = queryset.filter(department=department)
    if job_title:
        queryset = queryset.filter(job_title=job_title)
    if work_name:
        queryset = queryset.filter(work_name__icontains=work_name)    
    if type_wagon:
        # Handle filtering for default wagon type which represents null/empty entries
        if type_wagon == DEFAULT_WAGON_TYPE:
            queryset = queryset.filter(type_wagon__isnull=True)
        else:
            queryset = queryset.filter(type_wagon=type_wagon)
    return queryset
