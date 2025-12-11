from django.urls import reverse
from django.utils import timezone

from employee.forms import DailySalaryForm
from employee.models import Employee
from employee.utils.select_department import get_selected_department
from employee.utils.selects import get_distinct_values


def build_daily_salary_context(request):
    """Build context for daily salary creation view."""
    department = get_selected_department(request)

    # Filter employees by selected department, or show none if not selected
    employees = Employee.objects.none()
    if department:
        employees = Employee.objects.filter(department=department, is_active=True).order_by('employee_id')

    # Get distinct job titles for filtering dropdown
    job_titles = get_distinct_values(Employee, 'job_title', department, department_field='department')

    return {
        'form': DailySalaryForm(),
        'object_type': 'Daily Salary',
        'employees': employees,
        'errors': [],
        'today': timezone.now().date(),
        'selected_department': department,
        'cancel_url': reverse('daily_salary_list'),
        'job_titles': job_titles,
    }
