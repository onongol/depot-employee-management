def is_in_group(request, group_name):
    """Returns True if the user is authenticated and belongs to the specified group."""
    return request.user.is_authenticated and request.user.groups.filter(name=group_name).exists()


def is_employee(request):
    """Context processor to check if the user is an employee."""
    return {'is_employee': is_in_group(request, 'Employees')}


def is_master(request):
    """Context processor to check if the user is a master."""
    return {'is_master': is_in_group(request, 'Masters')}


def is_payroll(request):
    """Context processor to check if the user is a payroll specialist."""
    return {'is_payroll': is_in_group(request, 'Payrolls')}
