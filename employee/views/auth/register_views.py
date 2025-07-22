from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import Group  # Import Group model
from django.contrib import messages


def register_view(request):
    """User registration view."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Add user to Employees group automatically
            group, created = Group.objects.get_or_create(name='Employees')
            user.groups.add(group)
            # Do NOT log in the user automatically
            messages.success(request, "Registration successful! Please log in with your new account.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})
