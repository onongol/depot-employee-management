from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class CustomAuthenticationForm(AuthenticationForm):
    """Login form relabeled for email, since self-registered users log in
    with their email (register_view sets username = email). Kept as a
    CharField, not EmailField, so existing non-email usernames (e.g. staff
    accounts) can still log in.
    """

    username = forms.CharField(
        label=_("Email"),
        widget=forms.TextInput(attrs={"class": "form-control", "autofocus": True}),
    )
