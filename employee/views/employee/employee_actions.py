from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from employee.models import Employee
from employee.services.admin_log_entries import log_object_change
from employee.utils.access import is_admin


def _set_employee_active_status(request, pk, is_active):
    employee = get_object_or_404(Employee, pk=pk)
    with transaction.atomic():
        employee.is_active = is_active
        employee.save()
        log_object_change(request.user, employee, changed_fields=["is_active"])
    return redirect(reverse("employee_list"))


@login_required(login_url="login")
@user_passes_test(is_admin, login_url="login")
def employee_activate(request, pk):
    return _set_employee_active_status(request, pk, True)


@login_required(login_url="login")
@user_passes_test(is_admin, login_url="login")
def employee_deactivate(request, pk):
    return _set_employee_active_status(request, pk, False)
