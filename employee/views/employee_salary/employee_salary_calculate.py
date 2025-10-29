from collections import defaultdict
from django.db.models import Sum

from employee.models import DailySalary
from employee.models import Piecework
from employee.utils.filters import filter_month_year


def employee_salary_calculate(employees, month, year):
    """Calculate employee salaries based on daily salary records and piecework using aggregation."""
    
    # Get sums of daily salaries
    salary_qs = DailySalary.objects.filter(employee__in=employees)
    salary_qs = filter_month_year(salary_qs, month=month, year=year)
    salary_groups = (
        salary_qs
        .values('employee', 'salary_date__year', 'salary_date__month')
        .annotate(total_salary_day=Sum('salary_day'))
    )

    # Get sums of piecework amounts
    piecework_qs = Piecework.objects.filter(employee__in=employees)

    # filter by month and year if provided
    if month:
        piecework_qs = piecework_qs.filter(work_date__month=month)
    if year:
        piecework_qs = piecework_qs.filter(work_date__year=year)

    # Apply month_period filter if provided
    piecework_groups = (
        piecework_qs
        .values('employee', 'work_date__year', 'work_date__month')
        .annotate(total_piecework_amount=Sum('amount_price'),
                  total_piecework_time=Sum('amount_time')
        )
    )

    # Group data by employees, years and months
    salary_data = defaultdict(dict)
    for group in salary_groups:
        key = (group['employee'], group['salary_date__year'], group['salary_date__month'])
        salary_data[key]['total_salary_day'] = group['total_salary_day'] or 0

    for group in piecework_groups:
        key = (group['employee'], group['work_date__year'], group['work_date__month'])
        salary_data[key]['total_piecework_amount'] = group['total_piecework_amount'] or 0
        salary_data[key]['total_piecework_time'] = group['total_piecework_time'] or 0

    # Prepare final salary data
    employee_salaries = []
    for employee in employees:
        for key in salary_data:
            emp_id, group_year, group_month = key
            # Match only the current employee
            if emp_id != employee.employee_id:
                continue
            # Calculate total salary
            total_salary_day = salary_data[key].get('total_salary_day', 0)
            total_piecework_amount = salary_data[key].get('total_piecework_amount', 0)
            total_piecework_time = salary_data[key].get('total_piecework_time', 0)
            total_salary = round(total_salary_day + total_piecework_amount, 2)
            
            # Append to results
            employee_salaries.append(
                {
                    'employee': employee,
                    'department': employee.department,
                    'month': group_month,
                    'year': group_year,
                    'total_salary_day': round(total_salary_day, 2),
                    'total_piecework_amount': round(total_piecework_amount, 2),
                    'total_piecework_time': round(total_piecework_time, 2),
                    'total_salary': total_salary,
                }
            )

    return employee_salaries
