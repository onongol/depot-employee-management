from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from employee.models import Employee
from employee.utils.select_department import get_selected_department


DEPARTMENTS = [
    'Механик', 
    'Авто хяналтын бүс (АКП)', 
    'Засвар 1', 
    'Засвар 2', 
    'Хос дугуй', 
    'Тэргэнцэр', 
    'Авто угсраа'
]


@receiver(user_logged_in)
def set_department_on_login(sender, user, request, **kwargs):
    """Set the department in the session when a user logs in."""
    try:
        employee = Employee.objects.get(user=user, is_active=True)
        if employee.department in DEPARTMENTS:
            request.session['department'] = employee.department
        else:
            request.session['department'] = None
    except Employee.DoesNotExist:
        request.session['department'] = None


@login_required(login_url='login')
def set_department(request):
    """Set the department in the user's session."""
    department = get_selected_department(request)
    if department in DEPARTMENTS:
        request.session['department'] = department
    else:
        request.session['department'] = None
    return redirect(request.META.get('HTTP_REFERER', '/'))
