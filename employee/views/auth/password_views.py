from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class CustomPasswordChangeView(PasswordChangeView):
    """Logs out the user after a successful password change and redirects to home."""
    template_name = 'auth/password_change.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """If the form is valid, save the new password, log out the user and redirect."""
        # Save the form (change password)
        form.save()
        # Optional: add a success message
        messages.success(self.request, _("Password changed successfully. Please sign in with your new password."))
        # Log out to force re-authentication
        logout(self.request)
        return redirect(self.get_success_url())
