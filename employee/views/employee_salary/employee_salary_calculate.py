from collections import defaultdict
from django.db.models import Sum

from employee.models import DailySalary
from employee.utils.filters import filter_month_year


def employee_salary_calculate(employees, month, year):
    """Calculate employee salaries based on daily salary records using aggregation."""
    # Fetch all DailySalary records for selected employees and period in a single query
    salary_groups = DailySalary.objects.filter(employee__in=employees)
    salary_groups = filter_month_year(salary_groups, month=month, year=year)
    # Aggregate total salary_day per employee per month and year
    salary_groups = (
        salary_groups
        .values('employee', 'salary_date__year', 'salary_date__month')
        .annotate(total_salary_day=Sum('salary_day'))
    )

    # Group salary data by employee
    salary_data = defaultdict(list)
    for group in salary_groups:
        salary_data[group['employee']].append(group)

    employee_salaries = []
    for employee in employees:
        for group in salary_data.get(employee.employee_id, []):
            group_month = group['salary_date__month']
            group_year = group['salary_date__year']

            # Use model methods to calculate salary components for this period
            total_salary_day = employee.get_total_salary_day(group_month, group_year)
            total_piecework_amount = employee.get_total_piecework_amount(group_month, group_year)
            total_salary = employee.get_total_salary(group_month, group_year)

            # Append the calculated data to the result list
            employee_salaries.append(
                {
                    'employee': employee,
                    'department': employee.department,
                    'month': group_month,
                    'year': group_year,
                    'total_salary_day': round(total_salary_day, 2),
                    'total_piecework_amount': round(total_piecework_amount, 2),
                    'total_salary': total_salary,
                }
            )

    return employee_salaries
