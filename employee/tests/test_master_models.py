import pytest
from django.core.exceptions import ValidationError

from employee.tests.factories import MasterFactory


@pytest.mark.django_db
def test_master_clean_rejects_duplicate_active_master_id():
    MasterFactory(master_id=42)

    duplicate = MasterFactory.build(master_id=42)
    with pytest.raises(ValidationError):
        duplicate.full_clean()

    original = MasterFactory(master_id=99)
    original.full_clean()


@pytest.mark.django_db
def test_master_clean_allows_duplicate_master_id_when_existing_is_soft_deleted():
    MasterFactory(master_id=42, is_deleted=True)

    new_master = MasterFactory.build(master_id=42, is_deleted=False)

    new_master.full_clean()  # must not raise


@pytest.mark.django_db
def test_master_save_uniqueness():
    MasterFactory(master_id=42)

    with pytest.raises(ValidationError):
        MasterFactory(master_id=42)
