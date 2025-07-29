from django.shortcuts import render, redirect
from django.contrib.auth.models import Group 
from django.contrib import messages

from employee.forms.register_forms import CustomUserCreationForm
from employee.models import Employee
from employee.models.master_models import Master  
from employee.models.payroll_models import Payroll


def link_user_to_instance(user, instance, group_name):
    """Link user to the given instance and assign the appropriate group."""
    group, _ = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)
    instance.user = user
    instance.save()


def register_view(request):
    """User registration view."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            register_id = form.cleaned_data.get('employee_id')
            user = None
            for model, id_field, group_name, not_found_msg in [
                (Employee, 'employee_id', 'Employees', ("Employee not found.")),
                (Master, 'master_id', 'Masters', ("Master not found.")),
                (Payroll, 'payroll_id', 'Payrolls', ("Payroll not found.")),
            ]:
                try:
                    instance = model.objects.get(**{id_field: register_id})
                    if instance.user:
                        form.add_error('employee_id', ("A user is already linked to this ID."))
                        return render(request, 'auth/register.html', {'form': form})
                    user = form.save()
                    link_user_to_instance(user, instance, group_name)
                    messages.success(request, ("Registration successful! Please log in with your new account."))
                    return redirect('login')
                except model.DoesNotExist:
                    continue
            form.add_error('employee_id', ("Employee, Master, or Payroll not found."))
            return render(request, 'auth/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})
