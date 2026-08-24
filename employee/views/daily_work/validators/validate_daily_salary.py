from django.utils.translation import gettext_lazy as _

from employee.models import DailySalary, Employee


def validate_daily_salary(selected_employee_ids, work_date):
    """Validate that all selected employees have a DailySalary record for the given work_date."""
    # Ensure all selected employees have DailySalary for the work_date
    employees_salary = DailySalary.objects.select_related("employee").filter(
        employee_code__in=selected_employee_ids,
        salary_date=work_date,
    )

    # Identify employees missing DailySalary records
    employees_with_salary_ids = {str(ds.employee_code) for ds in employees_salary}

    # Find employees without DailySalary
    missing_salary_employees = [
        emp
        for emp in Employee.objects.filter(employee_id__in=selected_employee_ids)
        if str(emp.employee_id) not in employees_with_salary_ids
    ]

    # Initialize error list
    errors = []

    # If any employees are missing DailySalary, add an error message
    if missing_salary_employees:
        missing_names = [str(emp) for emp in missing_salary_employees]
        errors.append(
            _(
                "Please create daily attendance for %(employees)s on %(date)s before proceeding."
            )
            % {"employees": ", ".join(missing_names), "date": work_date}
        )

    return employees_salary, errors
