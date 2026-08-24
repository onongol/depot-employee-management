from employee.models import Employee
from employee.utils.select_department import get_selected_department
from employee.utils.selects import get_distinct_values
from employee.views.employee.employee_context import EmployeeContext


def employee_prepare(request) -> EmployeeContext:
    department = get_selected_department(request)

    # Without view_employee a user only ever sees their own record.
    if request.user.has_perm("employee.view_employee"):
        employees = Employee.objects.for_user(request.user).filter(
            department=department
        )
    else:
        employees = Employee.objects.filter(user=request.user)

    employee_id = request.GET.get("employee_id")
    employee_name = request.GET.get("employee_name")
    job_title = request.GET.get("job_title")
    order_by = request.GET.get("order_by")
    direction = request.GET.get("direction")

    job_titles = get_distinct_values(Employee, "job_title", department)

    return EmployeeContext(
        employees=employees,
        selected_department=department,
        employee_id=employee_id,
        employee_name=employee_name,
        job_title=job_title,
        order_by=order_by,
        direction=direction,
        job_titles=job_titles,
    )
