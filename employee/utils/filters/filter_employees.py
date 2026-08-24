def filter_employees(queryset, context):
    """Reusable filter for Employee queryset."""
    employee_id = context.employee_id
    employee_name = context.employee_name
    job_title = context.job_title

    if employee_id:
        queryset = queryset.filter(employee_id=employee_id)
    if employee_name:
        queryset = queryset.filter(employee_name__icontains=employee_name)
    if job_title:
        queryset = queryset.filter(job_title=job_title)
    return queryset
