from employee.models import Employee


def get_employee_entries(results):
    """
    Returns a sorted list of unique employee display names (object_name),
    e.g. "(ID: 1) S.Name", for all unique employee_code(employee_id) values
    found in results.
    """
    employee_codes = {
        result["employee_code"] for result in results if result.get("employee_code")
    }

    employees_map = {
        employee.employee_id: str(employee)
        for employee in Employee.objects.filter(employee_id__in=employee_codes)
    }

    entries = {
        employees_map.get(
            result["employee_code"],
            f"(ID: {result.get('employee_code')}) {result.get('employee_name', '')}",
        )
        for result in results
        if result.get("employee_code")
    }

    return sorted(entries)
