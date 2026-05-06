from employee.models.daily_salary_models import DailySalary
from employee.utils.converting_date import format_date


def create_daily_salary_instance(emp, salary_date, hours_per_day):
    normalized_salary_date = (
        format_date(salary_date) if isinstance(salary_date, str) else salary_date
    )
    salary_day = float(hours_per_day) * float(emp.money_per_hour)

    return DailySalary(
        employee=emp,
        employee_code=emp.employee_id,
        employee_name=emp.employee_name,
        department=emp.department,
        job_title=emp.job_title,
        salary_date=normalized_salary_date,
        salary_year=normalized_salary_date.year if normalized_salary_date else None,
        salary_month=normalized_salary_date.month if normalized_salary_date else None,
        hours_per_day=hours_per_day,
        salary_day=salary_day,
    )
