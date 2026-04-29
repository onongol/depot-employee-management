from employee.constants.constants import (
    IS_EMPLOYEE_KEY,
    IS_MASTER_KEY,
    IS_PAYROLL_KEY,
)


def get_user_groups(request) -> set[str]:
    """Returns cached user groups for the current request."""
    if not hasattr(request, "_cached_user_groups"):
        request._cached_user_groups = set(
            request.user.groups.values_list("name", flat=True)
        )
    return request._cached_user_groups


def is_employee(request) -> bool:
    return getattr(request, "user_roles", {}).get(IS_EMPLOYEE_KEY, False)


def is_master(request) -> bool:
    return getattr(request, "user_roles", {}).get(IS_MASTER_KEY, False)


def is_payroll(request) -> bool:
    return getattr(request, "user_roles", {}).get(IS_PAYROLL_KEY, False)
