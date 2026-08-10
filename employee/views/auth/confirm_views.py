from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django_smart_ratelimit import rate_limit

from employee.forms.register_forms import ResendConfirmationForm
from employee.models import RegistrationRequest
from employee.views.auth.ratelimit import ratelimit_key
from employee.views.auth.services import (
    find_instance_by_id,
    link_user_to_instance,
    send_registration_confirmation_email,
)
from employee.views.auth.tokens import registration_confirm_token_generator

User = get_user_model()


def register_confirm_view(request, uidb64, token):
    """Confirm a pending registration and link the user to their record."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid, is_active=False)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not registration_confirm_token_generator.check_token(
        user, token
    ):
        messages.error(request, _("This confirmation link is invalid or has expired."))
        return redirect("register")

    try:
        registration_request = user.registration_request
    except RegistrationRequest.DoesNotExist:
        messages.error(request, _("This confirmation link is invalid or has expired."))
        return redirect("register")

    instance, group_name = find_instance_by_id(registration_request.register_id)
    if not instance or instance.user:
        messages.error(
            request,
            _("This ID is no longer available. Please contact your administrator."),
        )
        return redirect("register")

    user.is_active = True
    user.save(update_fields=["is_active"])
    link_user_to_instance(user, instance, group_name)
    registration_request.confirmed_at = timezone.now()
    registration_request.save(update_fields=["confirmed_at"])

    messages.success(request, _("Your account has been confirmed. Please sign in."))
    return redirect("login")


@rate_limit(key=ratelimit_key("register_resend"), rate="3/h")
def register_resend_view(request):
    """Resend the confirmation email for a pending registration."""
    if request.method == "POST":
        form = ResendConfirmationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.filter(email__iexact=email, is_active=False).first()
            if user is not None:
                registration_request = getattr(user, "registration_request", None)
                if registration_request and not registration_request.confirmed_at:
                    send_registration_confirmation_email(request, user)

            # Always show the same message so this can't be used to probe
            # which emails have a pending registration.
            messages.success(
                request,
                _(
                    "If an account with that email is pending confirmation, "
                    "a new email has been sent."
                ),
            )
            return redirect("login")
    else:
        form = ResendConfirmationForm()
    return render(request, "auth/register_resend.html", {"form": form})
