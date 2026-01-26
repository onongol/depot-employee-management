from collections import defaultdict

from employee.views.employee_salary.aggregate_piecework import aggregate_piecework
from employee.views.employee_salary.build_employee_salary import build_employee_salary
from employee.views.employee_salary.include_daily_salary import add_daily_salary
from employee.views.employee_salary.merge_piecework import merge_piecework
from employee.views.employee_salary.piecework_queries import build_piecework_qs


def employee_salary_calculate(
    employees,
    context,
    wagon_number: str | None = None,
    include_daily_salary: bool = False,
):
    """Calculate employee salary totals from piecework, optionally merging DailySalary aggregates."""
    month = context.month
    year = context.year
    group_by_wagon = context.wagon_mode

    qs = build_piecework_qs(
        employees=employees,
        month=month,
        year=year,
        group_by_wagon=group_by_wagon,
        wagon_number=wagon_number,
    )

    piecework_groups = aggregate_piecework(qs, group_by_wagon=group_by_wagon)

    salary_data = defaultdict(dict)

    # Optionally include DailySalary aggregates
    if include_daily_salary:
        add_daily_salary(
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

    employee_salaries = build_employee_salary(
        salary_data=salary_data, employees=employees
    )

    return employee_salaries
