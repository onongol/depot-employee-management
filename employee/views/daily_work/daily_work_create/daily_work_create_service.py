from employee.views.daily_work.daily_work_create.calculation.calculate_piecework_records import (
    calculate_piecework_records,
)
from employee.views.daily_work.daily_work_create.daily_work_create_entries import (
    daily_work_create_entries,
)
from employee.views.daily_work.daily_work_create.piecework_create_bulk import (
    piecework_create_bulk,
)
from employee.views.daily_work.validators.validate_create import CreateValidator


def create_daily_work_piecework_records(request_data):
    """Process piecework creation based on the request data."""
    work_date = request_data.work_date
    type_work = request_data.type_work
    wagon_number = request_data.wagon_number
    selected_work_ids = request_data.selected_work_ids
    amounts = request_data.amounts
    job_title = request_data.job_title

    validator = CreateValidator(request_data)

    employees_salary, errors = validator.validate()

    # After validation the input data
    if errors:
        return None, None, errors

    # Create Daily_Work
    daily_works, works_dict = daily_work_create_entries(
        selected_work_ids, amounts, job_title, type_work, wagon_number, work_date
    )

    # Calculate Piecework records
    pieceworks, errors = calculate_piecework_records(
        employees_salary=employees_salary,
        selected_work_ids=selected_work_ids,
        amounts=amounts,
        works_dict=works_dict,
        work_date=work_date,
        type_work=type_work,
        wagon_number=wagon_number,
    )
    errors.extend(errors)

    # After calculating piecework and additional checks
    if errors:
        return None, None, errors

    # Create mapping of employees from validated salary list to avoid per-row queries
    employees_map = {
        str(daily_salary.employee.employee_id): daily_salary.employee
        for daily_salary in employees_salary
    }

    # Create Piecework
    piecework_create_bulk(pieceworks, daily_works, works_dict, employees_map, errors)

    return pieceworks, works_dict, errors
