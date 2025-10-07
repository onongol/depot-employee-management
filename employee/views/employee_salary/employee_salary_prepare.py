
from employee.models import Employee


def employee_salaries_prepare(request):
    """Prepare the base queryset and filter parameters for employee salaries."""
    # Extract filter parameters from the request
    employee_id = request.GET.get('employee_id', '')    
    employee_name = request.GET.get('employee_name', '')
    department = request.GET.get('department', '')
    job_title = request.GET.get('job_title', '')
    # Unified month period (primary) or fallback to legacy ?month & ?year
    raw_month_period = (request.GET.get('month_period', '') or '').strip()

    # Parse month_period if provided
    month = year = ''
    month_period = ''

    if raw_month_period:
        # Primary param
        try:
            y, m = raw_month_period.split('-')
            year = int(y)
            month = int(m)
            month_period = f"{year:04d}-{month:02d}"
        except ValueError:
            pass
    else:
        # Legacy separate params
        raw_month = request.GET.get('month', '').strip()
        raw_year = request.GET.get('year', '').strip()
        #if raw_month or raw_year:
            #log.warning("DEPRECATED salary filter: use month_period=YYYY-MM instead of month/year (got month=%s year=%s)", raw_month, raw_year)
        if raw_month.isdigit() and raw_year.isdigit():
            year = int(raw_year)
            month = int(raw_month)
            month_period = f"{year:04d}-{month:02d}"
    
    # Query all employees and prefetch related DailySalary data for efficiency
    if request.user.groups.filter(name='Employees').exists():
        # If the user is an employee, filter only their record
        employees = Employee.objects.filter(user=request.user, is_active=True)
    else:
        # Otherwise, get all active employees
        employees = Employee.objects.filter(is_active=True)

    return employees, employee_id, employee_name, department, job_title, month, year, month_period
