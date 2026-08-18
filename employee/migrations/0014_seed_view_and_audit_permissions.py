from django.contrib.auth.management import create_permissions
from django.db import migrations

# Per-model view_* rights mean "sees everyone's records, not just my own" —
# they drive both the list querysets and the filter panels. Payrolls and
# Masters get them; the Employees group deliberately does not.
# (view_employee was already seeded in 0012.)
SHARED = [
    ("dailysalary", "view_dailysalary"),
    ("dailywork", "view_dailywork"),
    ("piecework", "view_piecework"),
    ("work", "view_work"),
    # record_date (audit) columns and filters, app-wide.
    ("piecework", "view_record_audit"),
]

# Money stays with Payrolls only: Masters see hours, not salary amounts.
PAYROLLS_ONLY = [
    ("dailysalary", "view_salary_amount"),
]


def _ensure_permissions_exist(apps):
    # view_record_audit / view_salary_amount are declared in 0013; on a fresh
    # DB post_migrate has not fired yet when this RunPython runs, so create
    # them from the migration-time model state instead of waiting for it.
    app_config = apps.get_app_config("employee")
    app_config.models_module = True
    create_permissions(app_config, apps=apps, verbosity=0)
    app_config.models_module = None


def _get_permission(apps, app_model, codename):
    ContentType = apps.get_model("contenttypes", "ContentType")
    Permission = apps.get_model("auth", "Permission")
    content_type = ContentType.objects.get(app_label="employee", model=app_model)
    return Permission.objects.get(content_type=content_type, codename=codename)


def seed_permissions(apps, schema_editor):
    _ensure_permissions_exist(apps)

    Group = apps.get_model("auth", "Group")

    payrolls_group, _ = Group.objects.get_or_create(name="Payrolls")
    masters_group, _ = Group.objects.get_or_create(name="Masters")

    shared_perms = [_get_permission(apps, *item) for item in SHARED]
    payrolls_perms = [_get_permission(apps, *item) for item in PAYROLLS_ONLY]

    payrolls_group.permissions.add(*shared_perms, *payrolls_perms)
    masters_group.permissions.add(*shared_perms)


def unseed_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")

    shared_perms = [_get_permission(apps, *item) for item in SHARED]
    payrolls_perms = [_get_permission(apps, *item) for item in PAYROLLS_ONLY]

    Group.objects.get(name="Payrolls").permissions.remove(
        *shared_perms, *payrolls_perms
    )
    Group.objects.get(name="Masters").permissions.remove(*shared_perms)


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0013_alter_dailysalary_options_alter_piecework_options"),
    ]

    operations = [
        migrations.RunPython(seed_permissions, unseed_permissions),
    ]
