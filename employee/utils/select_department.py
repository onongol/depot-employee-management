def get_selected_department(request):
    """Get the selected department from request or session."""
    return getattr(request, "selected_department", None) or request.GET.get(
        "department"
    )
