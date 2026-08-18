from django.contrib.auth.management import create_permissions
from django.db import migrations

# Payrolls only: Employees and Masters stay locked to the department on their
# own Employee/Master record.
GROUPS = ["Payrolls"]


def _ensure_permissions_exist(apps):
    # select_department is declared in 0015; on a fresh DB post_migrate has not
    # fired yet when this RunPython runs, so create it from the migration-time
    # model state instead of waiting for it.
    app_config = apps.get_app_config("employee")
    app_config.models_module = True
    create_permissions(app_config, apps=apps, verbosity=0)
    app_config.models_module = None


def _get_permission(apps):
    ContentType = apps.get_model("contenttypes", "ContentType")
    Permission = apps.get_model("auth", "Permission")
    content_type = ContentType.objects.get(app_label="employee", model="employee")
    return Permission.objects.get(
        content_type=content_type, codename="select_department"
    )


def seed_select_department(apps, schema_editor):
    _ensure_permissions_exist(apps)

    Group = apps.get_model("auth", "Group")
    permission = _get_permission(apps)

    for name in GROUPS:
        group, _ = Group.objects.get_or_create(name=name)
        group.permissions.add(permission)


def unseed_select_department(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    permission = _get_permission(apps)

    for name in GROUPS:
        Group.objects.get(name=name).permissions.remove(permission)


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0015_alter_employee_options"),
    ]

    operations = [
        migrations.RunPython(seed_select_department, unseed_select_department),
    ]
