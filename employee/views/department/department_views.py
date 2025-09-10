from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from employee.models import Employee
from employee.models import Master
from employee.utils.select_department import get_selected_department
from employee.constants.constants import DEPARTMENTS


def get_user_department(user):
    """Get the department of the user from Employee or Master models."""
    for model in (Employee, Master):
        try:
            obj = model.objects.get(user=user, is_active=True)
            if getattr(obj, 'department', None) in DEPARTMENTS:
                return obj.department
        except model.DoesNotExist:
            continue
    return None


@receiver(user_logged_in)
def set_department_on_login(sender, user, request, **kwargs):
    """Set the department in the session when a user logs in."""
    request.session['department'] = get_user_department(user)


@login_required(login_url='login')
def set_department(request):
    """Set the department in the user's session."""
    department = get_selected_department(request)
    if department in DEPARTMENTS:
        request.session['department'] = department
    else:
        request.session['department'] = None
    return redirect(request.META.get('HTTP_REFERER', '/'))
