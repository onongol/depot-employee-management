def build_employee_salary_list(*, salary_data, employees):
    """
    Convert aggregated salary_data into the final list of rows for the UI/report.
    This maps employee IDs back to Employee objects and calculates the final totals per (employee, year, month, wagon).
    """
    employee_by_id = {e.pk: e for e in employees}

    rows = []
    for (emp_id, group_year, group_month, wagon_number), data in salary_data.items():
        employee = employee_by_id.get(emp_id)
        if employee is None:
            continue

        total_salary_day = data.get("total_salary_day", 0)
        total_piecework_amount = data.get("total_piecework_amount", 0)
        total_piecework_time = data.get("total_piecework_time", 0)

        total_salary = round(total_salary_day + total_piecework_amount, 2)

        rows.append(
            {
                "employee": employee,
                "department": employee.department,
                "wagon_number": wagon_number,
                "month": group_month,
                "year": group_year,
                "total_salary_day": round(total_salary_day, 2),
                "total_piecework_amount": round(total_piecework_amount, 2),
                "total_piecework_time": round(total_piecework_time, 2),
                "total_salary": total_salary,
            }
        )

    return rows
