from employee.constants.constants import Department

ZASVAR_DEPARTMENTS = {Department.ZASVAR_1.value, Department.ZASVAR_2.value}


def expand_department(department: str):
    """Return list of departments to query for the selected department."""
    if not department:
        return []
    if department in ZASVAR_DEPARTMENTS:
        return list(ZASVAR_DEPARTMENTS)
    return [department]


def get_selected_department(request):
    """Get the selected department from request or session."""
    return request.GET.get('department') or request.session.get('department')
