import pytest
from django.core.exceptions import ValidationError

from employee.tests.factories import EmployeeFactory


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
def test_employee_save_does_not_enforce_uniqueness_without_full_clean():
    # Unlike Work, Employee has no save() override that calls full_clean(),
    # and there's no UniqueConstraint on employee_id in Meta either — so
    # clean()'s duplicate check only ever runs if something explicitly calls
    # full_clean() (e.g. a ModelForm). Plain ORM usage — bulk scripts, data
    # imports, any Employee.objects.create() call — can silently create
    # duplicate active employee_ids.
    EmployeeFactory(employee_id=42)
    duplicate = EmployeeFactory(employee_id=42)  # no error, despite the duplicate

    assert duplicate.pk is not None
