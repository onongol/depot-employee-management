import pytest

from employee.constants.constants import GroupNames
from employee.tests.factories import UserFactory


@pytest.mark.django_db
def test_change_employee_status_true_for_payrolls_group_member():
    user = UserFactory(groups=[GroupNames.PAYROLLS.value])

    assert user.has_perm("employee.change_employee_status") is True


@pytest.mark.django_db
def test_change_employee_status_false_without_payrolls_group():
    # Masters is the "creator" group for add_* permissions but must not
    # grant this Payrolls-only permission.
    user = UserFactory(groups=[GroupNames.MASTERS.value])

    assert user.has_perm("employee.change_employee_status") is False


@pytest.mark.django_db
def test_change_employee_status_true_for_superuser_without_any_group():
    user = UserFactory(is_superuser=True)

    assert user.has_perm("employee.change_employee_status") is True


@pytest.mark.django_db
def test_view_material_report_true_for_payrolls_group_member():
    user = UserFactory(groups=[GroupNames.PAYROLLS.value])

    assert user.has_perm("employee.view_material_report") is True


@pytest.mark.django_db
def test_view_material_report_false_without_payrolls_group():
    user = UserFactory(groups=[GroupNames.MASTERS.value])

    assert user.has_perm("employee.view_material_report") is False


@pytest.mark.django_db
def test_add_piecework_true_for_payrolls_or_masters_group_member():
    # add_piecework is granted to both groups (the old is_creator behavior),
    # unlike the two Payrolls-only permissions above.
    for group_name in (GroupNames.PAYROLLS.value, GroupNames.MASTERS.value):
        user = UserFactory(groups=[group_name])
        assert user.has_perm("employee.add_piecework") is True


@pytest.mark.django_db
def test_add_piecework_false_without_payrolls_or_masters_group():
    user = UserFactory(groups=[GroupNames.EMPLOYEES.value])

    assert user.has_perm("employee.add_piecework") is False
