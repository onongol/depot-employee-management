from django.contrib.auth.management import create_permissions
from django.db import migrations

# (content_type.model, codename) pairs. Kept as module-level constants so
# forward and reverse reference the exact same set.
PAYROLLS_ONLY = [
    ("dailywork", "delete_dailywork"),
    ("dailywork", "change_dailywork"),
    ("work", "delete_work"),
    ("work", "add_work"),
    ("work", "change_work"),
    ("employee", "change_employee_status"),
    ("employee", "delete_employee"),
    ("employee", "add_employee"),
    ("employee", "change_employee"),
    ("piecework", "view_material_report"),
    ("piecework", "change_piecework"),
    ("dailysalary", "delete_dailysalary"),
    ("dailysalary", "change_dailysalary"),
]
PAYROLLS_AND_MASTERS = [
    ("piecework", "add_piecework"),
    ("dailywork", "add_dailywork"),
    ("dailysalary", "add_dailysalary"),
]


def _ensure_permissions_exist(apps):
    # post_migrate only fires once, after every migration in this `migrate`
    # invocation has applied — on a fresh DB (new clone, CI) that means the
    # Permission rows for change_employee_status/view_material_report don't
    # exist yet when this RunPython runs. Force-create them from the
    # historical (migration-time) model state instead of waiting for it.
    app_config = apps.get_app_config("employee")
    app_config.models_module = True
    create_permissions(app_config, apps=apps, verbosity=0)
    app_config.models_module = None


def _get_permission(apps, app_model, codename):
    ContentType = apps.get_model("contenttypes", "ContentType")
    Permission = apps.get_model("auth", "Permission")
    content_type = ContentType.objects.get(app_label="employee", model=app_model)
    return Permission.objects.get(content_type=content_type, codename=codename)


def seed_group_permissions(apps, schema_editor):
    _ensure_permissions_exist(apps)

    Group = apps.get_model("auth", "Group")

    payrolls_group, _ = Group.objects.get_or_create(name="Payrolls")
    masters_group, _ = Group.objects.get_or_create(name="Masters")

    payrolls_perms = [
        _get_permission(apps, *item) for item in PAYROLLS_ONLY + PAYROLLS_AND_MASTERS
    ]
    masters_perms = [_get_permission(apps, *item) for item in PAYROLLS_AND_MASTERS]

    payrolls_group.permissions.add(*payrolls_perms)
    masters_group.permissions.add(*masters_perms)


def unseed_group_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")

    payrolls_perms = [
        _get_permission(apps, *item) for item in PAYROLLS_ONLY + PAYROLLS_AND_MASTERS
    ]
    masters_perms = [_get_permission(apps, *item) for item in PAYROLLS_AND_MASTERS]

    Group.objects.get(name="Payrolls").permissions.remove(*payrolls_perms)
    Group.objects.get(name="Masters").permissions.remove(*masters_perms)


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0009_employee_change_employee_status_permission"),
        ("employee", "0010_piecework_view_material_report_permission"),
    ]

    operations = [
        migrations.RunPython(seed_group_permissions, unseed_group_permissions),
    ]
