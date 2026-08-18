from types import SimpleNamespace

import pytest
from django.contrib.auth.models import AnonymousUser

from employee.constants.constants import GroupNames
from employee.tests.factories import UserFactory
from employee.utils.user_roles import is_employee


def _request(user):
    return SimpleNamespace(user=user)


@pytest.mark.django_db
def test_is_employee_true_when_in_employees_group():
    user = UserFactory(groups=[GroupNames.EMPLOYEES.value])
    assert is_employee(_request(user)) is True


@pytest.mark.django_db
def test_is_employee_false_without_any_group():
    user = UserFactory()
    assert is_employee(_request(user)) is False


@pytest.mark.django_db
def test_is_employee_false_for_superuser_without_employees_group():
    # Unlike access.is_payroll/is_creator, this role check has no
    # is_superuser bypass at all: a superuser not in the Employees group
    # gets no special treatment here — the two "role check" systems in this
    # codebase disagree about what a superuser is entitled to.
    user = UserFactory(is_superuser=True)
    assert is_employee(_request(user)) is False


@pytest.mark.django_db
def test_is_employee_true_with_multiple_groups_including_employees():
    user = UserFactory(groups=[GroupNames.EMPLOYEES.value, GroupNames.MASTERS.value])
    assert is_employee(_request(user)) is True


def test_is_employee_false_for_anonymous_user():
    # get_user_groups short-circuits on is_authenticated before touching
    # .groups, so this needs no DB access at all.
    assert is_employee(_request(AnonymousUser())) is False
