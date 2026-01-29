# employee/utils/calculate.py
def calculate_salary_percentages(employees_salary):
    """
    Calculate each employee's percentage share of the total salary;
    if the total is zero, assign 0% to all to avoid division by zero
    """
    total = sum(emp.salary_day for emp in employees_salary)

    if total > 0:
        return {
            emp.employee.employee_id: round((emp.salary_day / total) * 100, 2)
            for emp in employees_salary
        }
    else:
        return {emp.employee.employee_id: 0 for emp in employees_salary}
