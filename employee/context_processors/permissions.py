from employee.constants.constants import (
    EMPLOYEE_GROUP,
    IS_EMPLOYEE_KEY,
    IS_MASTER_KEY,
    IS_PAYROLL_KEY,
    MASTER_GROUP,
    PAYROLL_GROUP,
)
from employee.utils.user_roles import get_user_groups


def user_roles(request):
    """Context processor to check all user roles at once with a single SQL query (cached)."""
    if not request.user.is_authenticated:
        return {
            IS_EMPLOYEE_KEY: False,
            IS_MASTER_KEY: False,
            IS_PAYROLL_KEY: False,
        }

    groups = get_user_groups(request)

    return {
        IS_EMPLOYEE_KEY: EMPLOYEE_GROUP in groups,
        IS_MASTER_KEY: MASTER_GROUP in groups,
        IS_PAYROLL_KEY: PAYROLL_GROUP in groups,
    }
