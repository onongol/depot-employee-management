from employee.constants.constants import GroupNames


def is_payroll(user):
    """Check if user is in Payrolls group or is a superuser."""
    return (
        user.is_superuser or user.groups.filter(name=GroupNames.PAYROLLS.value).exists()
    )


def is_creator(user):
    """Check if user is in Payrolls or Masters groups or is a superuser."""
    return (
        user.is_superuser
        or user.groups.filter(
            name__in=[GroupNames.PAYROLLS.value, GroupNames.MASTERS.value]
        ).exists()
    )
