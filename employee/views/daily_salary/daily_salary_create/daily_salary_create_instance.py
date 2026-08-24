from employee.models.daily_salary_models import DailySalary


def create_daily_salary_instance(emp, salary_date, hours_per_day):
    # salary_date is a date by here: the view parses it and
    # validate_daily_salary_required rejects None before this runs.
    salary_day = float(hours_per_day) * float(emp.money_per_hour)

    return DailySalary(
        employee=emp,
        employee_code=emp.employee_id,
        employee_name=emp.employee_name,
        department=emp.department,
        job_title=emp.job_title,
        salary_date=salary_date,
        salary_year=salary_date.year,
        salary_month=salary_date.month,
        hours_per_day=hours_per_day,
        salary_day=salary_day,
    )
