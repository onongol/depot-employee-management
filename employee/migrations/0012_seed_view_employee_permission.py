from django.db import migrations

# view_employee means "sees more than their own record" — it drives both the
# employee_list queryset and the filter panel. Payrolls and Masters get it;
# the Employees group deliberately does not.
GROUPS = ["Payrolls", "Masters"]


def _get_permission(apps):
    ContentType = apps.get_model("contenttypes", "ContentType")
    Permission = apps.get_model("auth", "Permission")
    content_type = ContentType.objects.get(app_label="employee", model="employee")
    return Permission.objects.get(content_type=content_type, codename="view_employee")


def seed_view_employee(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    permission = _get_permission(apps)

    for name in GROUPS:
        group, _ = Group.objects.get_or_create(name=name)
        group.permissions.add(permission)


def unseed_view_employee(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    permission = _get_permission(apps)

    for name in GROUPS:
        Group.objects.get(name=name).permissions.remove(permission)


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0011_seed_group_permissions"),
    ]

    operations = [
        migrations.RunPython(seed_view_employee, unseed_view_employee),
    ]
