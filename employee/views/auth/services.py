from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import pre_save
from django.dispatch import receiver

from employee.constants.constants import GroupNames
from employee.models import Employee, Master, Payroll

REGISTERABLE_MODELS = [
    (Employee, GroupNames.EMPLOYEES.value),
    (Master, GroupNames.MASTERS.value),
    (Payroll, GroupNames.PAYROLLS.value),
]


def link_user_to_instance(user, instance, group_name):
    """Link user to the given instance and assign the appropriate group."""
    group, _ = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)
    instance.user = user
    instance.save()


def find_instance_by_email(email):
    """Find the instance and corresponding group by the given email."""
    for model, group_name in REGISTERABLE_MODELS:
        instance = model.objects.filter(email__iexact=email).first()
        if instance:
            return instance, group_name
    return None, None


def link_confirmed_email_to_instance(sender, request, email_address, **kwargs):
    """allauth `email_confirmed` receiver: links the HR record now it's verified."""
    instance, group_name = find_instance_by_email(email_address.email)
    if instance and not instance.user:
        link_user_to_instance(email_address.user, instance, group_name)


@receiver(pre_save, sender=get_user_model())
def sync_username_to_email(sender, instance, **kwargs):
    """Keep username == email so django-axes' failure and success paths agree on who logged in (AXES_RESET_ON_SUCCESS needs this to match)."""
    if instance.email:
        instance.username = instance.email


def get_display_name(user):
    """The linked HR record's name (source of truth); one select_related query since this runs on every page load."""
    profiles = [
        ("employee_profile", "employee_name"),
        ("master_profile", "master_name"),
        ("payroll_profile", "payroll_name"),
    ]
    joined = (
        get_user_model()
        .objects.select_related(*(related_name for related_name, _ in profiles))
        .get(pk=user.pk)
    )
    for related_name, name_field in profiles:
        profile = getattr(joined, related_name, None)
        if profile:
            return getattr(profile, name_field)
    return user.get_full_name() or user.username
