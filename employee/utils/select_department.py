def get_selected_department(request):
    """Get the selected department from request or session."""
    return request.GET.get("department") or request.session.get("department")
