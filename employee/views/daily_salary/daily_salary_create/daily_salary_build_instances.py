from employee.views.daily_salary.daily_salary_create.daily_salary_create_instance import (
    create_daily_salary_instance,
)
from employee.views.daily_salary.validators.validate_duplicate import (
    validate_daily_salary_duplicate,
)


def build_daily_salary_instances(
    *,
    selected_ids,
    employees_dict,
    existing_records,
    salary_date,
    hours_per_day,
    errors,
):
    """
    For each selected employee, check for existing daily salary records to prevent duplicates; if none exist, calculate the salary and prepare a new DailySalary instance.
    """
    new_records = []

    for emp_id in selected_ids:
        emp = employees_dict.get(emp_id)

        if validate_daily_salary_duplicate(
            emp_id, emp, existing_records, salary_date, errors
        ):
            continue

        record = create_daily_salary_instance(emp, salary_date, hours_per_day)
        new_records.append(record)

    return new_records
