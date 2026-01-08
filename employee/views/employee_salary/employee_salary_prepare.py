
from employee.models import Employee

from employee.utils.month_period import parse_month_period


def employee_salaries_prepare(request):
    """Prepare the base queryset and filter parameters for employee salaries."""
    # Extract filter parameters from the request
    employee_id = request.GET.get('employee_id', '')    
    employee_name = request.GET.get('employee_name', '')
    department = request.GET.get('department', '')
    job_title = request.GET.get('job_title', '')

    month, year, month_period = parse_month_period(request) 
    
    # Query all employees and prefetch related DailySalary data for efficiency
    if request.user.groups.filter(name='Employees').exists():
        # If the user is an employee, filter only their record
        employees = Employee.objects.filter(user=request.user, is_active=True)
    else:
        # Otherwise, get all active employees
        employees = Employee.objects.filter(is_active=True)

    return employees, employee_id, employee_name, department, job_title, month, year, month_period
