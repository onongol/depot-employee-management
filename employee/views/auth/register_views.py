from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from employee.forms.register_forms import CustomUserCreationForm
from employee.views.auth.services import find_instance_by_id, link_user_to_instance


def register_view(request):
    """User registration view."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            register_id = form.cleaned_data.get("employee_id")

            # Try to find the corresponding instance (Employee, Master, or Payroll) by ID
            instance, group_name = find_instance_by_id(register_id)
            if instance:
                # Check if this instance is already linked to a user
                if instance.user:
                    form.add_error(
                        "employee_id", _("An account with this ID already exists.")
                    )
                else:
                    user = form.save()
                    link_user_to_instance(user, instance, group_name)
                    messages.success(
                        request,
                        _(
                            "Registration successful. Please sign in."
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
