from django.db.models import Sum

from employee.models import DailySalary


def aggregate_daily_salary(*, salary_data, employees, month, year) -> None:
    """
    Merge DailySalary aggregates into salary_data.
    Important:
      - DailySalary has no wagon_number, so it can only be grouped by (employee, year, month).
      - When the UI groups by wagon, DailySalary will always belong to the "no wagon" bucket (wagon=None),
        which is typically rendered as '-' in the table.
    """

    salary_qs = DailySalary.objects.filter(employee__in=employees)

    if month:
        salary_qs = salary_qs.filter(salary_month=month)
    if year:
        salary_qs = salary_qs.filter(salary_year=year)

    salary_groups = salary_qs.values(
        "employee", "salary_year", "salary_month"
    ).annotate(total_salary_day=Sum("salary_day"))

    for group in salary_groups:
        key = (
            group["employee"],
            group["salary_year"],
            group["salary_month"],
            None,
        )
        salary_data[key]["total_salary_day"] = group["total_salary_day"] or 0
