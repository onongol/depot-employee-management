from employee.views.daily_work.daily_work_create.calculation.calculate_salary_percentages import (
    calculate_salary_percentages,
)
from employee.views.daily_work.daily_work_create.calculation.calculate_work_amount_price import (
    calculate_work_amount_price,
)
from employee.views.daily_work.daily_work_create.post_data.post_data_context import (
    PostData,
)
from employee.views.daily_work.validators.validate_parse_amount import (
    validate_parse_amount,
)


def calculate_piecework_records(
    post_data: PostData,
    *,
    employees_salary,
    works_dict,
):
    """
    Calculate and validate piecework data for each employee and work.
    Returns (results, errors):
      - results: list of dicts with calculated data (not saved to DB)
      - errors: list of error messages
    """
    errors = []
    results = []

    employee_percentages = calculate_salary_percentages(employees_salary)

    # For each employee and each selected work, validate the amount and calculate the piecework price; collect errors for missing or invalid amounts.
    for emp in employees_salary:
        emp_pk = emp.employee.id
        emp_code = emp.employee.employee_id
        percent = employee_percentages[emp_code]

        for work_id in post_data.selected_work_ids:
            work = works_dict.get(work_id)
            amount = post_data.amounts.get(work_id)

            amount_decimal = validate_parse_amount(amount, work, errors)
            if amount_decimal is None:
                continue

            amount_price = calculate_work_amount_price(
                work_price=work.price, percent=percent, amount_decimal=amount_decimal
            )

            results.append(
                {
                    "employee_id": emp_pk,
                    "employee_code": emp_code,
                    "work_id": work_id,
                    "amount": amount_decimal,
                    "amount_price": amount_price,
                    "work_date": post_data.work_date,
                    "type_work": post_data.type_work,
                    "wagon_number": post_data.wagon_number,
                }
            )

    return results, errors
