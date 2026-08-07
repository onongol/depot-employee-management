from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from employee.constants.constants import GroupNames
from employee.models import Employee, Master, Payroll


def send_registration_confirmation_email(request, user):
    """Email a signed confirmation link for the user's pending registration."""
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    confirm_url = request.build_absolute_uri(
        reverse("register_confirm", kwargs={"uidb64": uid, "token": token})
    )
    message = render_to_string(
        "auth/email/registration_confirm.txt",
        {"user": user, "confirm_url": confirm_url},
    )
    send_mail(
        _("Confirm your registration"),
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )


def link_user_to_instance(user, instance, group_name):
    """Link user to the given instance and assign the appropriate group."""
    group, _ = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)
    instance.user = user
    instance.save()


def find_instance_by_id(register_id):
    """Find the instance and corresponding group by the given register ID."""
    for model, id_field, group_name in [
        (Employee, "employee_id", GroupNames.EMPLOYEES.value),
        (Master, "master_id", GroupNames.MASTERS.value),
        (Payroll, "payroll_id", GroupNames.PAYROLLS.value),
    ]:
        # Find the instance by ID
        instance = model.objects.filter(**{id_field: register_id}).first()
        if instance:
            return instance, group_name
    return None, None
