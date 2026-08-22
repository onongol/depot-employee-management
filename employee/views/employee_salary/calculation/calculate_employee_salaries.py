from collections import defaultdict

from employee.views.employee_salary.calculation.aggregate_daily_salary import (
    aggregate_daily_salary,
)
from employee.views.employee_salary.calculation.aggregate_piecework import (
    aggregate_piecework,
)
from employee.views.employee_salary.calculation.merge_piecework import (
    merge_piecework,
)
from employee.views.employee_salary.calculation.piecework_queries import (
    build_piecework,
)
from employee.views.employee_salary.calculation.salary_builders import (
    build_employee_salary_list,
)


def calculate_employee_salaries(
    employees,
    context,
    wagon_number: str | None = None,
    *,
    include_daily_salary: bool = False,
):
    """Calculate employee salary totals from piecework, optionally merging DailySalary aggregates."""
    month = context.month
    year = context.year
    group_by_wagon = context.wagon_mode

    # Evaluate queryset once so that piecework/daily_salary filters use IN (id, ...) instead of a subquery.
    employees = list(employees)

    piecework = build_piecework(
        employees=employees,
        month=month,
        year=year,
        group_by_wagon=group_by_wagon,
        wagon_number=wagon_number,
    )

    piecework_groups = aggregate_piecework(piecework, group_by_wagon=group_by_wagon)

    salary_data = defaultdict(dict)

    # Optionally include DailySalary aggregates
    if include_daily_salary:
        aggregate_daily_salary(
            salary_data=salary_data,
            employees=employees,
            month=month,
            year=year,
        )

    merge_piecework(
        salary_data,
        piecework_groups=piecework_groups,
        group_by_wagon=group_by_wagon,
    )

    return build_employee_salary_list(salary_data=salary_data, employees=employees)
