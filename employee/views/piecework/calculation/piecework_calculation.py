from decimal import Decimal

from django.utils.translation import gettext_lazy as _


def piecework_calculate_records(
    employees_salary,
    selected_work_ids,
    amounts,
    works_dict,
    work_date,
    type_work,
    wagon_number=None,
):
    """
    Calculate and validate piecework data for each employee and work.
    Returns (results, errors):
      - results: list of dicts with calculated data (not saved to DB)
      - errors: list of error messages
    """
    errors = []
    results = []

    # Calculate total salary for all employees in the selection
    employees_money_sum = sum(emp.salary_day for emp in employees_salary)

    # Calculate the percentage of each employee's salary relative to the total
    employee_percentages = {}
    if employees_money_sum > 0:
        for emp in employees_salary:
            employee_percentages[emp.employee.employee_id] = round(
                (emp.salary_day / employees_money_sum) * 100, 2
            )
    else:
        # If total salary is zero, set all percentages to zero to avoid division by zero
        for emp in employees_salary:
            employee_percentages[emp.employee.employee_id] = 0

    # Iterate over each employee and each selected work to calculate piecework data
    for emp in employees_salary:
        emp_id = emp.employee.employee_id
        percent = employee_percentages[emp_id]
        for work_id in selected_work_ids:
            amount = amounts.get(work_id)
            if not amount:
                # If amount is missing for a work, add an error and skip
                work = works_dict.get(work_id)
                errors.append(
                    _("Amount required for work %(work_name)s.")
                    % {"work_name": work.work_name}
                )
                continue
            try:
                amount_decimal = Decimal(amount)
            except Exception:
                # If amount is not a valid decimal, add an error and skip
                work = works_dict.get(work_id)
                errors.append(
                    _("Invalid amount for work %(work_name)s.")
                    % {"work_name": work.work_name}
                )
                continue

            work = works_dict.get(work_id)

            # Calculate amount_price
            value = round((work.price * percent) / 100, 2)
            amount_price = round(value * amount_decimal, 2)

            # Collect all calculated data for later saving
            results.append(
                {
                    "employee_id": emp_id,
                    "work_id": work_id,
                    "amount": amount_decimal,
                    "amount_price": amount_price,
                    "work_date": work_date,
                    "type_work": type_work,
                    "wagon_number": wagon_number,
                }
            )
    return results, errors
