from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
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
                "min": "1",
            }
        ),
        help_text=_("Enter your ID to sync your profile."),
    )

    username = forms.CharField(
        label=_("Username"),
        max_length=150,
    )

    email = forms.EmailField(
        label=_("Email"),
        required=True,
        help_text=_("Must match profile email."),
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(),
        help_text=_("Minimum of 8 characters."),
    )

    password2 = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput(),
        strip=False,
    )

    class Meta:
        model = get_user_model()
        fields = ("employee_id", "username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("An account with this email already exists."))
        return email


class ResendConfirmationForm(forms.Form):
    """Requests a new confirmation email for a pending registration."""

    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
