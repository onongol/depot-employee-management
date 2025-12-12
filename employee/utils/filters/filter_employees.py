def filter_employees(queryset, department=None, employee_id=None, employee_name=None, job_title=None):
    """Reusable filter for Employee queryset."""
    if department:
        queryset = queryset.filter(department=department)
    if employee_id:
        queryset = queryset.filter(employee_id=employee_id)
    if employee_name:
        queryset = queryset.filter(name__icontains=employee_name)
    if job_title:
        queryset = queryset.filter(job_title=job_title)
    return queryset
