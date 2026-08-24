import pytest
from django.core.exceptions import ValidationError

from employee.tests.factories import EmployeeFactory, MasterFactory, PayrollFactory

SOFT_DELETE_UNIQUE_MODELS = [
    pytest.param(EmployeeFactory, "employee_id", id="Employee"),
    pytest.param(MasterFactory, "master_id", id="Master"),
    pytest.param(PayrollFactory, "payroll_id", id="Payroll"),
]


@pytest.mark.django_db
@pytest.mark.parametrize(("factory", "id_field"), SOFT_DELETE_UNIQUE_MODELS)
def test_clean_rejects_a_duplicate_active_id(factory, id_field):
    factory(**{id_field: 42})

    duplicate = factory.build(**{id_field: 42})

    with pytest.raises(ValidationError):
        duplicate.full_clean()


@pytest.mark.django_db
@pytest.mark.parametrize(("factory", "id_field"), SOFT_DELETE_UNIQUE_MODELS)
def test_clean_does_not_let_an_unchanged_instance_conflict_with_itself(
    factory, id_field
):
    original = factory(**{id_field: 99})

    original.full_clean()  # must not raise


@pytest.mark.django_db
@pytest.mark.parametrize(("factory", "id_field"), SOFT_DELETE_UNIQUE_MODELS)
def test_clean_allows_a_duplicate_id_when_the_existing_row_is_soft_deleted(
    factory, id_field
):
    factory(**{id_field: 42, "is_deleted": True})

    new_record = factory.build(**{id_field: 42, "is_deleted": False})

    new_record.full_clean()  # must not raise


@pytest.mark.django_db
@pytest.mark.parametrize(("factory", "id_field"), SOFT_DELETE_UNIQUE_MODELS)
def test_restore_fails_when_the_id_was_taken_while_the_row_was_deleted(
    factory, id_field
):
    # restore() goes through save() -> full_clean(), and by then the freed id
    # belongs to someone else. The row stays deleted instead of resurfacing as
    # a duplicate.
    deleted = factory(**{id_field: 42})
    deleted.delete()
    factory(**{id_field: 42})

    with pytest.raises(ValidationError):
        deleted.restore()

    assert type(deleted).all_objects.get(pk=deleted.pk).is_deleted is True


@pytest.mark.django_db
@pytest.mark.parametrize(("factory", "id_field"), SOFT_DELETE_UNIQUE_MODELS)
def test_save_enforces_uniqueness_without_an_explicit_full_clean(factory, id_field):
    # save() calls full_clean() itself, so a plain create() is guarded too —
    # ModelForms are not the only entry point that has to stay safe.
    factory(**{id_field: 42})

    with pytest.raises(ValidationError):
        factory(**{id_field: 42})
