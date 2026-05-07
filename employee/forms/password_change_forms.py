from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(),
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(),
        strip=False,
        help_text=_("Minimum of 8 characters."),
    )

    new_password2 = forms.CharField(
        label=_("Confirm new password"),
        strip=False,
        widget=forms.PasswordInput(),
    )
