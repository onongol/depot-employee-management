from dataclasses import asdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from employee.utils.filters import filter_employees
from employee.utils.pagination import paginate_queryset
from employee.utils.sorting import apply_ordering
from employee.views.employee.employee_prepare import employee_prepare


@login_required(login_url="login")
def employee_list(request):
    """View to list employees. Workers see only their own record."""
    e_context = employee_prepare(request)

    employees = e_context.employees

    employees = filter_employees(employees, context=e_context)

    employees = apply_ordering(
        employees,
        e_context.order_by,
        e_context.direction,
        allowed_fields=["employee_id"],
        default=["employee_id"],
    )

    page_obj = paginate_queryset(request, employees)

    return render(
        request,
        "employee/employee_list.html",
        {
            **asdict(e_context),
            "employees": page_obj,
            "page_obj": page_obj,
        },
    )
