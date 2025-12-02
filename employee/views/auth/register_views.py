from django.shortcuts import render, redirect
from django.contrib.auth.models import Group 
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from employee.forms.register_forms import CustomUserCreationForm
from employee.models import Employee
from employee.models import Master  
from employee.models import Payroll
from employee.constants.constants import GroupNames


def link_user_to_instance(user, instance, group_name):
    """Link user to the given instance and assign the appropriate group."""
    group, _ = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)
    instance.user = user
    instance.save()


def find_instance_by_id(register_id):
    """Find the instance and corresponding group by the given register ID."""
    for model, id_field, group_name in [
        (Employee, 'employee_id', GroupNames.EMPLOYEES.value),
        (Master, 'master_id', GroupNames.MASTERS.value),
        (Payroll, 'payroll_id', GroupNames.PAYROLLS.value),
    ]:
        # Find the instance by ID
        instance = model.objects.filter(**{id_field: register_id}).first()
        if instance:
            return instance, group_name
    return None, None


def register_view(request):
    """User registration view."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            register_id = form.cleaned_data.get('employee_id')
            # Try to find the corresponding instance (Employee, Master, or Payroll) by ID
            instance, group_name = find_instance_by_id(register_id)
            if instance:
                # Check if this instance is already linked to a user
                if instance.user:
                    form.add_error('employee_id', _("A user with this ID already exists."))
                else:
                    user = form.save()
                    link_user_to_instance(user, instance, group_name)
                    messages.success(request, _("Registration successful! Please sing in with your new account."))
                    return redirect('login')
            else:
                form.add_error('employee_id', _("Your ID is not registered. Check your ID. Contact the administrator."))
        return render(request, 'auth/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})
