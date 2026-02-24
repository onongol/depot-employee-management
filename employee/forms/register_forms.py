from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    """User registration form with additional employee_id field."""

    employee_id = forms.IntegerField(
        label=_("Employee ID"),
        required=True,
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "min": "1",
            }
        ),
        help_text=_("Enter your ID to sync your profile."),
    )

    username = forms.CharField(
        label=_("Username"),
        max_length=150,
        help_text="",
    )

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=_("Minimum of 8 characters."),
    )

    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text="",
    )

    class Meta:
        model = User
        fields = ("employee_id", "username", "password1", "password2")
