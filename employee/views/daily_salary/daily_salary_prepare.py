from employee.forms.filter_forms import DailySalaryFilterForm
from employee.models import DailySalary, Employee
from employee.utils.select_department import get_selected_department
from employee.utils.selects import get_distinct_values
from employee.views.daily_salary.daily_salary_context import DailySalaryContext


def daily_salary_prepare(request) -> DailySalaryContext:
    department = get_selected_department(request)

    # Without view_dailysalary a user only ever sees their own records.
    if request.user.has_perm("employee.view_dailysalary"):
        daily_salaries = DailySalary.objects.filter(
            department=department, employee__is_active=True
        )
    else:
        daily_salaries = DailySalary.objects.filter(
            employee__user=request.user,
            department=department,
            employee__is_active=True,
        )

    daily_salaries = daily_salaries.select_related("employee")

    employee_code = request.GET.get("employee_code")
    employee_name = request.GET.get("employee_name")
    job_title = request.GET.get("job_title")
    dates = DailySalaryFilterForm.parse(request.GET)
    salary_date = dates.get("salary_date")
    record_date = dates.get("record_date")

    order_by = request.GET.get("order_by")
    direction = request.GET.get("direction")

    job_titles = get_distinct_values(Employee, "job_title", department)

    return DailySalaryContext(
        daily_salaries=daily_salaries,
        selected_department=department,
        employee_code=employee_code,
        employee_name=employee_name,
        job_title=job_title,
        salary_date=salary_date,
        record_date=record_date,
        order_by=order_by,
        direction=direction,
        job_titles=job_titles,
    )
