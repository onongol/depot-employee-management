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


def filter_works(queryset, department=None, work_name=None):
    """Reusable filter for Work queryset."""
    if department:
        queryset = queryset.filter(department__icontains=department)
    if work_name:
        queryset = queryset.filter(work_name__icontains=work_name)
    return queryset


def filter_daily_salaries(queryset, employee_id=None, employee_name=None, salary_date=None, record_date=None):
    """Reusable filter for DailySalary queryset."""
    if employee_id:
        queryset = queryset.filter(employee__employee_id=employee_id)
    if employee_name:
        queryset = queryset.filter(employee__name__icontains=employee_name)
    if salary_date:
        queryset = queryset.filter(salary_date=salary_date)
    if record_date:
        queryset = queryset.filter(record_date__date=record_date)
    return queryset

"""
def filter_pieceworks(queryset, filters):
    #Reusable filter for Piecework queryset.
    if filters.get('employee_id'):
        queryset = queryset.filter(employee__employee_id=filters['employee_id'])
    if filters.get('employee_name'):
        queryset = queryset.filter(employee__name__icontains=filters['employee_name'])
    if filters.get('work'):
        queryset = queryset.filter(work__work_name=filters['work'])
    if filters.get('type_work'):
        queryset = queryset.filter(type_work=filters['type_work'])
    if filters.get('type_material'):
        queryset = queryset.filter(work__type_material=filters['type_material'])
    if filters.get('work_date'):
        queryset = queryset.filter(work_date=filters['work_date'])
    if filters.get('record_date'):
        queryset = queryset.filter(record_date__date=filters['record_date'])
    return queryset
"""

def filter_pieceworks(queryset, employee_id=None, employee_name=None, work=None, type_work=None, type_material=None, work_date=None, record_date=None):
    """Reusable filter for Piecework queryset."""
    if employee_id:
        queryset = queryset.filter(employee__employee_id=employee_id)
    if employee_name:
        queryset = queryset.filter(employee__name__icontains=employee_name)
    if work:
        queryset = queryset.filter(work__work_name=work)
    if type_work:
        queryset = queryset.filter(type_work=type_work)
    if type_material:
        queryset = queryset.filter(work__type_material=type_material)
    if work_date:
        queryset = queryset.filter(work_date=work_date)
    if record_date:
        queryset = queryset.filter(record_date__date=record_date)
    return queryset


def filter_material(queryset, work_name=None, selected_type='all', start_date=None, end_date=None):
    """Reusable filter for Material queryset."""
    if work_name:
        queryset = queryset.filter(work__work_name__icontains=work_name)
    if selected_type and selected_type != 'all':
        queryset = queryset.filter(work__type_material=selected_type)
    if start_date:
        queryset = queryset.filter(work_date__gte=start_date)
    if end_date:
        queryset = queryset.filter(work_date__lte=end_date)
    return queryset


def filter_month_year(queryset, month=None, year=None):
    """Reusable filter for DailySalary queryset."""
    if month:
        queryset = queryset.filter(salary_date__month=int(month))
    if year:
        queryset = queryset.filter(salary_date__year=int(year))
    return queryset
