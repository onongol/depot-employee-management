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

    class Meta:
        model = User
        fields = ("employee_id", "username", "password1", "password2")
