def get_selected_department_from_request(request):
    """
    Get the selected department from request.GET or request.session and set it on request for reuse.
    """
    selected_dep = request.GET.get("department") or request.session.get("department")
    request.selected_department = selected_dep
    return selected_dep
