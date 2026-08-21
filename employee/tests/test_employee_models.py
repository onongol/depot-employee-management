import pytest

from employee.tests.factories import EmployeeFactory, UserFactory


@pytest.mark.django_db
def test_employee_save_syncs_linked_user_is_active_regardless_of_caller():
    linked_user = UserFactory(is_active=True)
    employee = EmployeeFactory(user=linked_user)

    employee.is_active = False
    employee.save()

    linked_user.refresh_from_db()
    assert linked_user.is_active is False


@pytest.mark.django_db
def test_employee_save_without_linked_user_does_not_crash():
    employee = EmployeeFactory(user=None)

    employee.is_active = False
    employee.save()  # must not raise
