from django.db.models import Q

from employee.utils.converting_date import parse_date_range
from employee.utils.select_department import expand_department
from employee.constants.constants import DEFAULT_WAGON_TYPE, DEFAULT_WAGON_NUMBER


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


def filter_works(queryset, department=None, job_title=None, work_name=None, type_wagon=None):
    """Reusable filter for Work queryset."""
    if department:
        # Expand the department to include all related departments
        departments = expand_department(department)
        if departments:
            queryset = queryset.filter(department__in=departments)
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


def filter_daily_works(queryset, job_title=None, work_name=None, type_work=None, wagon_number=None, type_wagon=None, type_material=None, work_date=None, record_date=None):
    """Reusable filter for DailyWork queryset."""
    if job_title:
        queryset =queryset.filter(job_title=job_title)   
    if work_name:
        queryset =queryset.filter(work__work_name__icontains=work_name)
    if type_work:
        queryset =queryset.filter(type_work=type_work)
    if wagon_number:
        if wagon_number == DEFAULT_WAGON_NUMBER:
            queryset = queryset.filter(Q(wagon_number__isnull=True))
        else:
            queryset = queryset.filter(wagon_number=wagon_number)
    if type_wagon:
        if type_wagon == DEFAULT_WAGON_TYPE:
            queryset =queryset.filter(type_wagon__isnull=True)
        else:
           queryset =queryset.filter(type_wagon=type_wagon)
    if type_material:
       queryset =queryset.filter(work__type_material=type_material)
    if work_date:
       queryset =queryset.filter(work_date=work_date)
    if record_date:
       queryset =queryset.filter(record_date__date=record_date)
    return queryset


def filter_pieceworks(queryset, employee_id=None, employee_name=None, job_title=None, work_name=None, type_work=None, wagon_number=None, type_wagon=None, type_material=None, range_date=None, record_date=None):
    """Reusable filter for Piecework queryset."""
    if employee_id:
        queryset = queryset.filter(employee__employee_id=employee_id)
    if employee_name:
        queryset = queryset.filter(employee__name__icontains=employee_name)
    if job_title:
        queryset = queryset.filter(job_title=job_title)   
    if work_name:
        queryset = queryset.filter(work__work_name__icontains=work_name)
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
    if type_material:
        queryset = queryset.filter(work__type_material=type_material)
    if range_date:
        start_date, end_date = parse_date_range(range_date)
        if start_date:
            queryset = queryset.filter(work_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(work_date__lte=end_date)
    if record_date:
        queryset = queryset.filter(record_date__date=record_date)
    return queryset


def filter_wagon(queryset, wagon_number=None, type_wagon=None, work_name=None, type_work=None, work_date=None):
    """Reusable filter for Wagon queryset."""
    if wagon_number:
        queryset = queryset.filter(wagon_number=wagon_number)
    if type_wagon:
        if type_wagon == DEFAULT_WAGON_TYPE:
            queryset = queryset.filter(type_wagon__isnull=True)
        else:
            queryset = queryset.filter(type_wagon=type_wagon)
    if work_name:
        queryset = queryset.filter(work__work_name__icontains=work_name)
    if type_work:
        queryset = queryset.filter(type_work=type_work)
    if work_date:
        queryset = queryset.filter(work_date=work_date)
    return queryset


def filter_material(queryset, work_name=None, type_material=None, range_date=None):
    """Reusable filter for Material queryset with date range."""
    if work_name:
        queryset = queryset.filter(work__work_name__icontains=work_name)
    if type_material:
        queryset = queryset.filter(work__type_material=type_material)
    if range_date:
        start_date, end_date = parse_date_range(range_date)
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
