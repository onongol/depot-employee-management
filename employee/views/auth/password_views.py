from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.shortcuts import redirect

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'auth/password_change.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        logout(self.request)
        return redirect(self.get_success_url())
    