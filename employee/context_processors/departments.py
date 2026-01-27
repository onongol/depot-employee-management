from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS, DEPARTMENTS


def global_departments(request):
    """Context processor to provide a list of distinct departments."""

    departments_list = sorted(DEPARTMENTS)

    if not departments_list:
        departments_list = ["No departments available"]
        
    return {
        "departments": departments_list,
        "ALLOWED_WAGON_DEPARTMENTS": ALLOWED_WAGON_DEPARTMENTS,
        "request": request,
    }
