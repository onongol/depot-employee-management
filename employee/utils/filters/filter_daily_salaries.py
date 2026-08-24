def filter_daily_salaries(queryset, context):
    """Reusable filter for DailySalary queryset."""
    employee_code = context.employee_code
    employee_name = context.employee_name
    job_title = context.job_title
    salary_date = context.salary_date
    record_date = context.record_date

    if employee_code:
        queryset = queryset.filter(employee_code=employee_code)
    if employee_name:
        queryset = queryset.filter(employee_name__icontains=employee_name)
    if job_title:
        queryset = queryset.filter(job_title=job_title)
    if salary_date:
        queryset = queryset.filter(salary_date=salary_date)
    if record_date:
        queryset = queryset.filter(record_date__date=record_date)
    return queryset
