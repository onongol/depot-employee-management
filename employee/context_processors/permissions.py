from employee.constants.constants import (
    EMPLOYEE_GROUP,
    IS_EMPLOYEE_KEY,
    IS_MASTER_KEY,
    IS_PAYROLL_KEY,
    MASTER_GROUP,
    PAYROLL_GROUP,
)
from employee.utils.user_roles import get_user_groups

ROLE_GROUP_MAP = {
    IS_EMPLOYEE_KEY: EMPLOYEE_GROUP,
    IS_MASTER_KEY: MASTER_GROUP,
    IS_PAYROLL_KEY: PAYROLL_GROUP,
}


def user_roles(request):
    """Context processor to check all user roles at once with a single SQL query (cached)."""
    if not request.user.is_authenticated:
        return {key: False for key in ROLE_GROUP_MAP}

    groups = get_user_groups(request)

    return {
        key: group_name in groups for key, group_name in ROLE_GROUP_MAP.items()
    }
