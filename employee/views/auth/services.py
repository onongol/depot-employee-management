from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from employee.constants.constants import GroupNames
from employee.models import Employee, Master, Payroll
from employee.views.auth.tokens import registration_confirm_token_generator


def send_registration_confirmation_email(request, user):
    """Email a signed confirmation link for the user's pending registration."""
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = registration_confirm_token_generator.make_token(user)
    confirm_url = request.build_absolute_uri(
        reverse("register_confirm", kwargs={"uidb64": uid, "token": token})
    )
    context = {"user": user, "confirm_url": confirm_url}
    text_body = render_to_string("auth/email/registration_confirm.txt", context)
    html_body = render_to_string("auth/email/registration_confirm.html", context)

    email = EmailMultiAlternatives(
        _("Confirm your registration"),
        text_body,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
    email.attach_alternative(html_body, "text/html")
    email.send()


def link_user_to_instance(user, instance, group_name):
    """Link user to the given instance and assign the appropriate group."""
    group, _ = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)
    instance.user = user
    instance.save()


# (model, id_field, group_name) for each registerable profile type, checked
# in this priority order.
REGISTERABLE_MODELS = [
    (Employee, "employee_id", GroupNames.EMPLOYEES.value),
    (Master, "master_id", GroupNames.MASTERS.value),
    (Payroll, "payroll_id", GroupNames.PAYROLLS.value),
]


def find_instance_by_id(register_id):
    """Find the instance and corresponding group by the given register ID."""
    for model, id_field, group_name in REGISTERABLE_MODELS:
        instance = model.objects.filter(**{id_field: register_id}).first()
        if instance:
            return instance, group_name
    return None, None


def find_instance_by_email(email):
    """Find the instance, group, and register ID by the given email."""
    for model, id_field, group_name in REGISTERABLE_MODELS:
        instance = model.objects.filter(email__iexact=email).first()
        if instance:
            return instance, group_name, getattr(instance, id_field)
    return None, None, None
