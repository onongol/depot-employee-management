import pytest

from employee.constants.constants import GroupNames
from employee.tests.factories import UserFactory
from employee.utils.access import is_creator, is_payroll


@pytest.mark.django_db
def test_is_payroll_true_for_superuser_without_any_group():
    user = UserFactory(is_superuser=True)
    assert is_payroll(user) is True


@pytest.mark.django_db
def test_is_payroll_false_without_group_or_superuser():
    user = UserFactory()
    assert is_payroll(user) is False


@pytest.mark.django_db
def test_is_payroll_true_when_payrolls_is_one_of_several_groups():
    user = UserFactory(groups=[GroupNames.EMPLOYEES.value, GroupNames.PAYROLLS.value])
    assert is_payroll(user) is True


@pytest.mark.django_db
def test_is_payroll_false_when_in_unrelated_groups_only():
    # Masters membership must not grant Payrolls-only access.
    user = UserFactory(groups=[GroupNames.EMPLOYEES.value, GroupNames.MASTERS.value])
    assert is_payroll(user) is False


@pytest.mark.django_db
def test_is_creator_true_for_superuser_without_any_group():
    user = UserFactory(is_superuser=True)
    assert is_creator(user) is True


@pytest.mark.django_db
def test_is_creator_true_when_in_masters_group_not_payrolls():
    # This is the whole point of is_creator vs is_payroll: Masters counts too.
    user = UserFactory(groups=[GroupNames.MASTERS.value])
    assert is_creator(user) is True


@pytest.mark.django_db
def test_is_creator_false_when_only_in_employees_group():
    user = UserFactory(groups=[GroupNames.EMPLOYEES.value])
    assert is_creator(user) is False
