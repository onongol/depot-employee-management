from employee.models import DailySalary, Employee
from employee.utils.converting_date import format_date
from employee.utils.select_department import get_selected_department
from employee.utils.selects import get_distinct_values
from employee.views.daily_salary.daily_salary_context import DailySalaryContext


def daily_salary_prepare(request) -> DailySalaryContext:
    department = get_selected_department(request)

    if request.user.groups.filter(name="Employees").exists():
        daily_salaries = DailySalary.objects.filter(
            employee__user=request.user,
            employee__department=department,
            employee__is_active=True,
        )
    else:
        daily_salaries = DailySalary.objects.filter(
            employee__department=department, employee__is_active=True
        )

    daily_salaries = daily_salaries.select_related("employee")

    employee_id = request.GET.get("employee_id")
    employee_name = request.GET.get("employee_name")
    job_title = request.GET.get("job_title")
    salary_date = format_date(request.GET.get("salary_date"))
    record_date = format_date(request.GET.get("record_date"))

    order_by = request.GET.get("order_by")
    direction = request.GET.get("direction")

    job_titles = get_distinct_values(
        Employee, "job_title", department, department_field="department"
    )

    return DailySalaryContext(
        daily_salaries=daily_salaries,
        department=department,
        employee_id=employee_id,
        employee_name=employee_name,
        job_title=job_title,
        salary_date=salary_date,
        record_date=record_date,
        order_by=order_by,
        direction=direction,
        job_titles=job_titles,
    )
