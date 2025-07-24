from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth import login
from django.contrib.auth.models import Group 
from django.contrib import messages

from employee.forms.register_forms import CustomUserCreationForm
from employee.models import Employee
from employee.models.master_models import Master  
from employee.models.payroll_models import Payroll


def register_view(request):
    """User registration view."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            register_id = form.cleaned_data.get('employee_id')

            # First try to find Employee
            try:
                employee = Employee.objects.get(employee_id=register_id)
                if employee.user:
                    form.add_error('employee_id', "A user is already linked to this Employee ID.")
                    return render(request, 'auth/register.html', {'form': form})
                user = form.save()
                group, _ = Group.objects.get_or_create(name='Employees')
                user.groups.add(group)
                employee.user = user
                employee.save()
                messages.success(request, "Registration successful! Please log in with your new account.")
                return redirect('login')
            except Employee.DoesNotExist:

                # If Employee not found, try Master
                try:
                    master = Master.objects.get(master_id=register_id)
                    if master.user:
                        form.add_error('employee_id', "A user is already linked to this Master ID.")
                        return render(request, 'auth/register.html', {'form': form})
                    user = form.save()
                    group, _ = Group.objects.get_or_create(name='Masters')
                    user.groups.add(group)
                    master.user = user
                    master.save()
                    messages.success(request, "Registration successful! Please log in with your new account.")
                    return redirect('login')
                except Master.DoesNotExist:

                    # If Master not found, try Payroll
                    try:
                        payroll = Payroll.objects.get(payroll_id=register_id)
                        if payroll.user:
                            form.add_error('employee_id', "A user is already linked to this Payroll ID.")
                            return render(request, 'auth/register.html', {'form': form})
                        user = form.save()
                        group, _ = Group.objects.get_or_create(name='Payrolls')
                        user.groups.add(group)
                        payroll.user = user
                        payroll.save()
                        messages.success(request, "Registration successful! Please log in with your new account.")
                        return redirect('login')
                    except Payroll.DoesNotExist:

                        # If Employee, Master, or Payroll not found, return error
                        form.add_error('employee_id', "Employee, Master, or Payroll not found.")
                        return render(request, 'auth/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})
