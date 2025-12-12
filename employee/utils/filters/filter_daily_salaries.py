def filter_daily_salaries(queryset, employee_id=None, employee_name=None,
job_title=None, salary_date=None, record_date=None):
    """Reusable filter for DailySalary queryset."""
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
