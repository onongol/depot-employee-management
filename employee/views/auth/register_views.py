from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from employee.forms.register_forms import CustomUserCreationForm
from employee.models import RegistrationRequest
from employee.views.auth.services import (
    find_instance_by_id,
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
            register_id = form.cleaned_data.get("employee_id")
            email = form.cleaned_data.get("email")

            # Try to find the corresponding instance (Employee, Master, or Payroll) by ID
            instance, group_name = find_instance_by_id(register_id)
            if instance:
                if instance.user:
                    form.add_error(
                        "employee_id", _("An account with this ID already exists.")
                    )
                elif not instance.email:
                    form.add_error(
                        "employee_id",
                        _(
                            "This ID has no email on file. Please contact your administrator."
                        ),
                    )
                elif instance.email.lower() != email.lower():
                    form.add_error(
                        "email",
                        _("This email does not match our records for this profile."),
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
                        messages.success(
                            request,
                            _(
                                "Registration received. Please check your email to confirm your account."
                            ),
                        )
                        return redirect("login")
            else:
                form.add_error(
                    "employee_id",
                    _(
                        "This ID is not registered. Please check for typos or contact your administrator for assistance."
                    ),
                )

        return render(request, "auth/register.html", {"form": form})
    else:
        form = CustomUserCreationForm()
    return render(request, "auth/register.html", {"form": form})
