from employee.views.daily_work.daily_work_create.post_data.post_data_context import (
    PostData,
)
from employee.views.daily_work.validators.validate_daily_salary import (
    validate_daily_salary,
)
from employee.views.daily_work.validators.validate_duplicate import validate_duplicate
from employee.views.daily_work.validators.validate_required import validate_required


class CreateValidator:
    """Wrapper that runs required / duplicate / daily-salary checks using PostData."""

    def __init__(self, data: PostData):
        self.data = data

    def validate(self) -> tuple[object | None, list[str]]:
        errors: list[str] = []

        # 1) required fields & amounts
        errors.extend(
            validate_required(
                self.data.selected_employee_ids,
                self.data.selected_work_ids,
                self.data.work_date,
                self.data.type_work,
                self.data.amounts,
            )
        )

        # 2) duplicate check (only if required passed)
        if not errors:
            errors.extend(
                validate_duplicate(
                    self.data.selected_employee_ids,
                    self.data.selected_work_ids,
                    self.data.work_date,
                    self.data.type_work,
                    self.data.wagon_number,
                )
            )

        # 3) daily salary validation (only if previous passed)
        employees_salary = None
        if not errors:
            employees_salary, salary_errors = validate_daily_salary(
                self.data.selected_employee_ids, self.data.work_date
            )
            errors.extend(salary_errors)

        return employees_salary, errors
