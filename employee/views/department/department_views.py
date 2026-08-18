from urllib.parse import urlsplit

from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.shortcuts import redirect

from employee.constants.constants import DEPARTMENTS
from employee.utils.request_department import get_user_department
from employee.utils.select_department import get_selected_department


@receiver(user_logged_in)
def set_department_on_login(sender, user, request, **kwargs):
    """Set the department in the session when a user logs in."""
    request.session["department"] = get_user_department(user)


@login_required
def set_department(request):
    """Set the department in the user's session."""
    department = get_selected_department(request)
    if department in DEPARTMENTS:
        request.session["department"] = department
    else:
        request.session["department"] = None

    referer = request.META.get("HTTP_REFERER", "/")
    redirect_path = urlsplit(referer).path or "/"
    return redirect(redirect_path)
