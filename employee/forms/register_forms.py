from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    employee_id = forms.CharField(
        label="Employee ID",
        required=True,
        help_text="Enter your Employee ID to link your account."
    )

    class Meta:
        model = User
        fields = ("employee_id", "username", "password1", "password2")
