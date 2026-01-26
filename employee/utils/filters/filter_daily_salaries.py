def filter_daily_salaries(queryset, context):
    """Reusable filter for DailySalary queryset."""
    employee_id = context.employee_id
    employee_name = context.employee_name
    job_title = context.job_title
    salary_date = context.salary_date
    record_date = context.record_date

    if employee_id:
        queryset = queryset.filter(employee__employee_id=employee_id)
    if employee_name:
        queryset = queryset.filter(employee__name__icontains=employee_name)
    if job_title:
        queryset = queryset.filter(employee__job_title=job_title)
    if salary_date:
        queryset = queryset.filter(salary_date=salary_date)
    if record_date:
        queryset = queryset.filter(record_date__date=record_date)
    return queryset
