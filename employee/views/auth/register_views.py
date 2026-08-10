from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from employee.forms.register_forms import CustomUserCreationForm
from employee.models import RegistrationRequest
from employee.views.auth.services import (
    find_instance_by_email,
    send_registration_confirmation_email,
)


def register_view(request):
    """User registration view.

    Creates an inactive user and emails a confirmation link; the user is only
    linked to their Employee/Master/Payroll record once that link is clicked
    (see register_confirm_view), so an unconfirmed signup never occupies the
    target record.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")

            # Find the corresponding instance (Employee, Master, or Payroll) by email
            instance, group_name, register_id = find_instance_by_email(email)
            if instance:
                if instance.user:
                    form.add_error(
                        "email", _("An account with this email already exists.")
                    )
                else:
                    user = form.save(commit=False)
                    user.username = email
                    user.email = email
                    user.is_active = False
                    try:
                        user.save()
                    except IntegrityError:
                        # username == email, so a concurrent registration
                        # with the same email hits the DB's unique
                        # constraint on username here.
                        form.add_error(
                            "email", _("An account with this email already exists.")
                        )
                    else:
                        RegistrationRequest.objects.create(
                            user=user,
                            register_id=register_id,
                            group_name=group_name,
                        )
                        send_registration_confirmation_email(request, user)
                        return redirect("register_done")
            else:
                form.add_error(
                    "email",
                    _(
                        "No profile found with this email. Please contact your administrator for assistance."
                    ),
                )

        return render(request, "auth/register.html", {"form": form})
    else:
        form = CustomUserCreationForm()
    return render(request, "auth/register.html", {"form": form})


def register_done_view(request):
    """Tells the user to check their email; shown right after registering."""
    return render(request, "auth/register_done.html")
