from employee.constants.constants import DEPARTMENTS


def get_selected_department_from_request(request):
    """
    Get the selected department from request.GET or request.session and set it on request for reuse.
    """
    selected_department = request.GET.get("department") or request.session.get(
        "department"
    )
    if selected_department not in DEPARTMENTS:
        selected_department = None
    request.selected_department = selected_department
    return selected_department
