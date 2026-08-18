import pytest
from django.core.exceptions import ValidationError

from employee.tests.factories import EmployeeFactory, UserFactory


@pytest.mark.django_db
def test_employee_clean_rejects_duplicate_active_employee_id():
    EmployeeFactory(employee_id=42)

    duplicate = EmployeeFactory.build(employee_id=42)
    with pytest.raises(ValidationError):
        duplicate.full_clean()

    # Re-validating an existing, unchanged instance must not self-conflict.
    original = EmployeeFactory(employee_id=99)
    original.full_clean()


@pytest.mark.django_db
def test_employee_clean_allows_duplicate_employee_id_when_existing_is_soft_deleted():
    EmployeeFactory(employee_id=42, is_deleted=True)

    new_employee = EmployeeFactory.build(employee_id=42, is_deleted=False)

    new_employee.full_clean()  # must not raise


@pytest.mark.django_db
def test_employee_save_uniqueness():
    EmployeeFactory(employee_id=42)

    with pytest.raises(ValidationError):
        EmployeeFactory(employee_id=42)


@pytest.mark.django_db
def test_employee_save_syncs_linked_user_is_active_regardless_of_caller():
    # Must fire from Employee.save() itself, not just the activate/deactivate
    # view — otherwise admin list_editable edits (which call .save() directly,
    # bypassing that view) leave the linked User able to log in.
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
