import logging
from django.utils.dateparse import parse_date


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


def filter_daily_pays(queryset, employee_id=None, employee_name=None,
job_title=None, salary_date=None, record_date=None):
    """Reusable filter for DailyPay queryset."""
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


def filter_pieceworks(queryset, employee_id=None, employee_name=None, job_title=None, work=None, type_work=None, wagon_number=None, type_material=None, work_date=None, record_date=None):
    """Reusable filter for Piecework queryset."""
    if employee_id:
        queryset = queryset.filter(employee__employee_id=employee_id)
    if employee_name:
        queryset = queryset.filter(employee__name__icontains=employee_name)
    if job_title:
        queryset = queryset.filter(employee__job_title=job_title)   
    if work:
        queryset = queryset.filter(work__work_name__icontains=work)
    if type_work:
        queryset = queryset.filter(type_work=type_work)
    if wagon_number:
        queryset = queryset.filter(wagon_number=wagon_number)
    if type_material:
        queryset = queryset.filter(work__type_material=type_material)
    if work_date:
        queryset = queryset.filter(work_date=work_date)
    if record_date:
        queryset = queryset.filter(record_date__date=record_date)
    return queryset


def filter_wagon(queryset, wagon_number=None, work_name=None, work_date=None):
    """Reusable filter for Wagon queryset."""
    if wagon_number:
        queryset = queryset.filter(wagon_number=wagon_number)
    if work_name:
        queryset = queryset.filter(work__work_name__icontains=work_name)
    if work_date:
        queryset = queryset.filter(work_date=work_date)
    return queryset


def filter_material(queryset, work_name=None, selected_type='all', range_date=None):
    """Reusable filter for Material queryset with date range."""
    if work_name:
        queryset = queryset.filter(work__work_name__icontains=work_name)
    if selected_type and selected_type != 'all':
        queryset = queryset.filter(work__type_material=selected_type)
    if range_date:
        try:
            # flatpickr " to "
            start_str, end_str = [d.strip() for d in range_date.split('to')]
            start_date = parse_date(start_str)
            end_date = parse_date(end_str)
            if start_date:
                queryset = queryset.filter(work_date__gte=start_date)
            if end_date:
                queryset = queryset.filter(work_date__lte=end_date)
        except Exception as e:
            logging.warning(f'Invalid date range: {range_date} ({e})')
    return queryset


def filter_month_year(queryset, month=None, year=None):
    """Reusable filter for DailySalary queryset."""
    if month:
        queryset = queryset.filter(salary_date__month=int(month))
    if year:
        queryset = queryset.filter(salary_date__year=int(year))
    return queryset
