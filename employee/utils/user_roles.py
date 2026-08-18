from employee.constants.constants import EMPLOYEE_GROUP


def get_user_groups(request) -> set[str]:
    """Returns cached user groups for the current request."""
    if not request.user.is_authenticated:
        return set()

    if not hasattr(request, "_cached_user_groups"):
        request._cached_user_groups = set(
            request.user.groups.values_list("name", flat=True)
        )
    return request._cached_user_groups


def is_employee(request) -> bool:
    return EMPLOYEE_GROUP in get_user_groups(request)


# def is_master(request) -> bool:
#    return MASTER_GROUP in get_user_groups(request)


# def is_payroll(request) -> bool:
#    return PAYROLL_GROUP in get_user_groups(request)
