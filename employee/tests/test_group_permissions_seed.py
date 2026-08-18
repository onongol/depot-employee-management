import pytest
from django.contrib.auth.models import Group

PAYROLLS_CODENAMES = {
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
    "view_employee",
    "view_material_report",
}
MASTERS_CODENAMES = {
    "add_dailysalary",
    "add_dailywork",
    "add_piecework",
    "view_employee",
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
