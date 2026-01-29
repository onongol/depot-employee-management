from dataclasses import asdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS, GROUP_WAGON
from employee.utils.filters import filter_employees_salary
from employee.utils.pagination import paginate_queryset
from employee.views.employee_salary.calculation.calculate_employee_salaries import (
    calculate_employee_salaries,
)
from employee.views.employee_salary.employee_salary_prepare import (
    employee_salaries_prepare,
)
from employee.views.employee_salary.employee_salary_sort import apply_ordering


@login_required(login_url="login")
def employee_salary_list(request):
    """View to list all employee salaries with filters and pagination."""
    es_context = employee_salaries_prepare(request)

    employees = es_context.employees

    employees = filter_employees_salary(employees, context=es_context)

    employee_salaries = calculate_employee_salaries(
        employees,
        context=es_context,
        wagon_number=es_context.wagon_number if es_context.wagon_mode else None,
    )

    apply_ordering(
        employee_salaries,
        context=es_context,
        allowed_fields=["employee_id", "month", "year"],
    )

    page_obj = paginate_queryset(request, employee_salaries)

    return render(
        request,
        "employee_salary/employee_salary_list.html",
        {
            **asdict(es_context),
            "employee_salaries": page_obj,
            "page_obj": page_obj,
            "ALLOWED_WAGON_DEPARTMENTS": ALLOWED_WAGON_DEPARTMENTS,
            "GROUP_WAGON": GROUP_WAGON,
        },
    )
