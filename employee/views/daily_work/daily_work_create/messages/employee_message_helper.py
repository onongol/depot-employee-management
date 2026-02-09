from employee.models import Employee


def get_employee_entries(results):
    """
    Returns a sorted list of unique employee display names (object_name),
    e.g. "(ID: 1) S.Name", for all unique employee_id values
    found in results.
    """
    employee_ids = {
        result["employee_id"] for result in results if result.get("employee_id")
    }

    employees_map = {
        employee.employee_id: str(employee)
        for employee in Employee.objects.filter(employee_id__in=employee_ids)
    }

    entries = {
        employees_map.get(
            result["employee_id"],
            f"(ID: {result['employee_id']}) {result.get('employee_name', '')}",
        )
        for result in results
        if result.get("employee_id")
    }

    return sorted(entries)
