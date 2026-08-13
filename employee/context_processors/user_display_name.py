from employee.views.auth.services import get_display_name


def user_display_name(request):
    """Context processor exposing the user's HR-record name for the navbar menu."""
    if not request.user.is_authenticated:
        return {"display_name": ""}
    return {"display_name": get_display_name(request.user)}
