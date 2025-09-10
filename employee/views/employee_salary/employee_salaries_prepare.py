from datetime import datetime

from employee.models import Employee


def employee_salaries_prepare(request):
    """Prepare the base queryset and filter parameters for employee salaries."""
    # Get the current year for default filtering
    current_year = datetime.now().year

    # Extract filter parameters from the request
    employee_id = request.GET.get('employee_id', '')    
    employee_name = request.GET.get('employee_name', '')
    department = request.GET.get('department', '')
    job_title = request.GET.get('job_title', '')
    month = request.GET.get('month', '')
    year = request.GET.get('year', str(current_year))

    # Query all employees and prefetch related DailySalary data for efficiency
    if request.user.groups.filter(name='Employees').exists():
        # If the user is an employee, filter only their record
        employees = Employee.objects.filter(user=request.user, is_active=True)
    else:
        # Otherwise, get all active employees
        employees = Employee.objects.filter(is_active=True)

    return employees, employee_id, employee_name, department, job_title, month, year, current_year
