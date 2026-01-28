from employee.models import Employee


def build_employee_entries(results):
    """
    Returns a sorted list of strings in the format "employee_id/employee_name"
    for all unique employee_id values found in results.
    """
    employee_ids = {
        result["employee_id"] for result in results if result.get("employee_id")
    }

    employees_map = {
        str(employee.employee_id): employee.name
        for employee in Employee.objects.filter(employee_id__in=employee_ids)
    }

    return sorted(
        f"{result['employee_id']}/{employees_map.get(str(result['employee_id']), result.get('employee_name', ''))}"
        for result in results
        if result.get("employee_id")
    )
