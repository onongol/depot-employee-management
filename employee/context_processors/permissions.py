EMPLOYEE_GROUP = "Employees"
MASTER_GROUP = "Masters"
PAYROLL_GROUP = "Payrolls"

IS_EMPLOYEE_KEY = "is_employee"
IS_MASTER_KEY = "is_master"
IS_PAYROLL_KEY = "is_payroll"


def user_roles(request):
    """Context processor to check all user roles at once with a single SQL query."""
    user = request.user

    if not user.is_authenticated:
        return {
            IS_EMPLOYEE_KEY: False,
            IS_MASTER_KEY: False,
            IS_PAYROLL_KEY: False,
        }

    user_group_names = set(user.groups.values_list("name", flat=True))

    return {
        IS_EMPLOYEE_KEY: EMPLOYEE_GROUP in user_group_names,
        IS_MASTER_KEY: MASTER_GROUP in user_group_names,
        IS_PAYROLL_KEY: PAYROLL_GROUP in user_group_names,
    }
