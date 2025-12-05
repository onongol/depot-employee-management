import json
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse
from django.utils import timezone

from employee.models import Employee
from employee.models import Piecework
from employee.models import Work
from employee.forms import PieceworkForm
from employee.utils.select_department import get_selected_department
from employee.utils.selects import get_distinct_values
from employee.utils.select_type_wagon import get_type_wagon_filter_values
from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS
from employee.utils.converting_date import format_date


def build_daily_piecework_context(request):
    """Build context for daily work and piecework views."""
    # Get the selected department from the request
    department = get_selected_department(request)

    # Get today's date
    today = timezone.now().date()

    # Determine work_date: prefer GET, then POST, fallback to today
    raw_work_date = request.GET.get('work_date') or request.POST.get('work_date')
    if not raw_work_date:
        work_date = today
    else:
        work_date = format_date(raw_work_date)
    if work_date is None:
        work_date = None

    # Filter employees and works by selected department.
    # Only include employees who have a DailySalary record for work_date.
    if department:
        employees = (
            Employee.objects
            .filter(department=department, is_active=True)
            .order_by('employee_id')
        )
        # If a work_date is provided, filter to employees with DailySalary on that date
        if work_date:
            employees = employees.filter(dailysalary__salary_date=work_date).distinct()
    else:
        employees = Employee.objects.none()

    # Expand department for works filtering
    works = (
        Work.objects.filter(department=department).order_by('work_name')
        if department else Work.objects.none()
    )

    # Get distinct job titles for filtering dropdown
    emp_job_titles = get_distinct_values(
        Employee, 'job_title', department, department_field='department'
    )
    work_job_titles = get_distinct_values(
        Work, 'job_title', extra_filters={'department': department} if department else None
    )

    # Combine and sort job titles from employees and works
    job_titles = sorted(set(list(emp_job_titles) + list(work_job_titles)))

    # Get distinct type_wagon for filtering dropdown if department allows wagons
    type_wagons = get_type_wagon_filter_values(department)

    # Fetch existing Piecework records for the department to prevent duplicates
    existing_pieceworks = list(
        Piecework.objects.filter(employee__department=department)
        .values('employee_id', 'work_id', 'type_work', 'work_date', 'wagon_number')
    )

    # Build and return the context dictionary
    return {
        'form': PieceworkForm(department=department),
        'object_type': 'Daily Work & Piecework',
        'employees': employees,
        'works': works,
        'today': today,
        'work_date': work_date,
        'errors': [],
        'selected_department': department,
        'cancel_url': reverse('daily_work_list'),
        'existing_pieceworks_json': json.dumps(existing_pieceworks, cls=DjangoJSONEncoder), # Pass existing records as JSON
        'job_titles': job_titles,
        'ALLOWED_WAGON_DEPARTMENTS': ALLOWED_WAGON_DEPARTMENTS,
        'type_wagons': type_wagons,
    }
