from decimal import ROUND_HALF_UP, Decimal

TWO = Decimal("0.01")


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

        total_salary_day = data.get("total_salary_day") or Decimal(0)
        total_piecework_amount = data.get("total_piecework_amount") or Decimal(0)
        total_piecework_time = data.get("total_piecework_time") or Decimal(0)

        total_salary = (total_salary_day + total_piecework_amount).quantize(
            TWO, rounding=ROUND_HALF_UP
        )

        rows.append(
            {
                "employee": employee,
                "department": employee.department,
                "wagon_number": wagon_number,
                "month": group_month,
                "year": group_year,
                "total_salary_day": total_salary_day.quantize(
                    TWO, rounding=ROUND_HALF_UP
                ),
                "total_piecework_amount": total_piecework_amount.quantize(
                    TWO, rounding=ROUND_HALF_UP
                ),
                "total_piecework_time": total_piecework_time.quantize(
                    TWO, rounding=ROUND_HALF_UP
                ),
                "total_salary": total_salary,
            }
        )

    return rows
