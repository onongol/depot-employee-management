from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from employee.models import DailySalary, Employee
from employee.utils.converting_date import format_date
from employee.utils.filters import filter_daily_salaries
from employee.utils.pagination import paginate_queryset
from employee.utils.select_department import get_selected_department
from employee.utils.selects import get_distinct_values
from employee.utils.sorting import apply_ordering


@login_required(login_url="login")
def daily_salary_list(request):
    """View to list all daily salaries with filtering and pagination."""
    department = get_selected_department(request)

    # Filter daily salaries by department
    if request.user.groups.filter(name="Employees").exists():
        daily_salaries = DailySalary.objects.filter(
            employee__user=request.user,
            employee__department=department,
            employee__is_active=True,
        )
    else:
        # If not an employee, show all daily salaries in the department
        daily_salaries = DailySalary.objects.filter(
            employee__department=department, employee__is_active=True
        )

    # Reduce DB queries in template
    daily_salaries = daily_salaries.select_related("employee")

    # Get distinct job titles for filtering dropdown
    job_titles = get_distinct_values(
        Employee, "job_title", department, department_field="department"
    )

    # Filtering by employee ID, name, salary date, and record date
    employee_id = request.GET.get("employee_id")
    employee_name = request.GET.get("employee_name")
    job_title = request.GET.get("job_title")
    salary_date = format_date(request.GET.get("salary_date"))
    record_date = format_date(request.GET.get("record_date"))

    # Apply filters to the daily salaries queryset using reusable filter functions
    daily_salaries = filter_daily_salaries(
        daily_salaries,
        employee_id=employee_id,
        employee_name=employee_name,
        job_title=job_title,
        salary_date=salary_date,
        record_date=record_date,
    )

    # Sorting
    order_by = request.GET.get("order_by")
    direction = request.GET.get("direction")

    daily_salaries = apply_ordering(
        daily_salaries,
        order_by,
        direction,
        allowed_fields=["salary_date", "record_date"],
        default=["-salary_date", "-record_date"],
    )

    # Paginate the results, 10 records per page
    page_obj = paginate_queryset(request, daily_salaries)

    # Preserve filter values in the context for template rendering
    filters = {
        "employee_id": employee_id or "",
        "employee_name": employee_name or "",
        "job_title": job_title or "",
        "salary_date": salary_date or "",
        "record_date": record_date or "",
    }

    return render(
        request,
        "daily_salary/daily_salary_list.html",
        {
            "daily_salaries": page_obj,
            "page_obj": page_obj,
            "selected_department": department,
            "job_titles": job_titles,
            "filters": filters,
        },
    )
