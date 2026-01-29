from employee.models.daily_salary_models import DailySalary


def create_daily_salary_instance(emp, emp_id, salary_date, hours_per_day):
    salary_day = float(hours_per_day) * float(emp.money_per_hour)

    return DailySalary(
        employee_id=emp_id,
        employee_name=emp.name,
        department=emp.department,
        salary_date=salary_date,
        hours_per_day=hours_per_day,
        salary_day=salary_day,
    )
