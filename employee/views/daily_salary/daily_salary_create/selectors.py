from employee.models import DailySalary, Employee


def select_employees_by_ids(employee_ids):
    """Return a dict mapping employee_id to Employee object."""
    return {
        emp.employee_id: emp
        for emp in Employee.objects.filter(employee_id__in=employee_ids)
    }


def select_existing_employee_ids(employee_ids, salary_date):
    """
    Returns a set of employee_ids that already have a DailySalary record for the given date.
    """
    return set(
        DailySalary.objects.filter(
            employee_id__in=employee_ids, salary_date=salary_date
        ).values_list("employee_id", flat=True)
    )
