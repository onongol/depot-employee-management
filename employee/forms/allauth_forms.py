from allauth.account.forms import (
    ChangePasswordForm,
    LoginForm,
    ReauthenticateForm,
    ResetPasswordKeyForm,
    SignupForm,
)
from django import forms
from django.utils.translation import gettext_lazy as _

from employee.views.auth.services import find_instance_by_email


class CustomLoginForm(LoginForm):
    """Drops the password field's auto-injected "Forgot your password?" help text."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].help_text = ""


class CustomReauthenticateForm(ReauthenticateForm):
    """Drops the password field's auto-injected "Forgot your password?" help text."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].help_text = ""


class ShortPasswordHelpMixin:
    """Shortens the password-validator help text and confirm-field label."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].help_text = _("Minimum of 8 characters.")
        self.fields["password2"].label = _("Confirm password")


class CustomSignupForm(ShortPasswordHelpMixin, SignupForm):
    """Only allows signup for known HR emails; skips the "already claimed" check so allauth's enumeration-safe flow handles duplicates instead of leaking it via a form error."""

    def clean_email(self):
        email = super().clean_email()
        instance, _group_name = find_instance_by_email(email)
        if not instance:
            raise forms.ValidationError(
                _(
                    "No profile found with this email. Please contact your "
                    "administrator for assistance."
                )
            )
        return email


class CustomResetPasswordKeyForm(ShortPasswordHelpMixin, ResetPasswordKeyForm):
    """Relabels password1/password2 to "New password"/"Confirm new password"."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = _("New password")
        self.fields["password2"].label = _("Confirm new password")


class CustomChangePasswordForm(ShortPasswordHelpMixin, ChangePasswordForm):
    """Relabels fields and drops the current-password field's reset-help text."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["oldpassword"].label = _("Current password")
        self.fields["oldpassword"].help_text = ""
        self.fields["password1"].label = _("New password")
        self.fields["password2"].label = _("Confirm new password")
