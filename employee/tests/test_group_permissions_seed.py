import pytest
from django.contrib.auth.models import Group

# "Sees everyone's records, not just my own" plus the record_date audit
# columns — held by Payrolls and Masters alike.
SHARED_CODENAMES = {
    "view_dailysalary",
    "view_dailywork",
    "view_employee",
    "view_piecework",
    "view_record_audit",
    "view_work",
}

PAYROLLS_CODENAMES = SHARED_CODENAMES | {
    "add_dailysalary",
    "add_dailywork",
    "add_employee",
    "add_piecework",
    "add_work",
    "change_dailysalary",
    "change_dailywork",
    "change_employee",
    "change_employee_status",
    "change_piecework",
    "change_work",
    "delete_dailysalary",
    "delete_dailywork",
    "delete_employee",
    "delete_work",
    "view_material_report",
    "view_salary_amount",
}
MASTERS_CODENAMES = SHARED_CODENAMES | {
    "add_dailysalary",
    "add_dailywork",
    "add_piecework",
}


@pytest.mark.django_db
def test_payrolls_group_has_exactly_the_seeded_permissions():
    group = Group.objects.get(name="Payrolls")

    codenames = set(group.permissions.values_list("codename", flat=True))

    assert codenames == PAYROLLS_CODENAMES


@pytest.mark.django_db
def test_masters_group_has_exactly_the_seeded_permissions():
    group = Group.objects.get(name="Masters")

    codenames = set(group.permissions.values_list("codename", flat=True))

    assert codenames == MASTERS_CODENAMES
