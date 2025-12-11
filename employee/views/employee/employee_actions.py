from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.translation import gettext_lazy as _

from employee.models import Employee
from employee.utils.permissions import is_admin


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def employee_activate(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.is_active = True
    employee.save()
    return redirect(reverse('employee_list'))


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def employee_deactivate(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.is_active = False
    employee.save()
    return redirect(reverse('employee_list'))
