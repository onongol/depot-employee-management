from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import Group  # Import Group model
from django.contrib import messages

from employee.forms.register_forms import CustomUserCreationForm
from employee.models import Employee


def register_view(request):
    """User registration view."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            employee_id = form.cleaned_data.get('employee_id')
            try:
                employee = Employee.objects.get(employee_id=employee_id)
                if employee.user:
                    form.add_error('employee_id', "A user is already linked to this Employee ID.")
                    return render(request, 'auth/register.html', {'form': form})
            except Employee.DoesNotExist:
                form.add_error('employee_id', "Employee not found.")
                return render(request, 'auth/register.html', {'form': form})

            user = form.save()
            group, created = Group.objects.get_or_create(name='Employees')
            user.groups.add(group)
            employee.user = user
            employee.save()
            messages.success(request, "Registration successful! Please log in with your new account.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})
