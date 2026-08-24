from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from employee.constants.constants import Department, TypeWagon
from employee.tests.factories import WorkFactory


@pytest.mark.django_db
def test_work_clean_resets_usage_material_when_type_material_is_empty():
    with_material = WorkFactory(
        work_name="With material",
        type_material="Metal",
        usage_material=Decimal("5.0000"),
    )
    without_material = WorkFactory(
        work_name="Without material",
        type_material="",
        usage_material=Decimal("5.0000"),
    )

    assert with_material.type_material == "Metal"
    assert with_material.usage_material == Decimal("5.0000")

    assert without_material.type_material is None
    # An empty type_material forces usage_material back to 0, discarding
    # whatever value was passed in — it's not just a default.
    assert without_material.usage_material == Decimal("0.0000")


@pytest.mark.django_db
def test_work_clean_zeroes_type_wagon_outside_allowed_departments():
    allowed = WorkFactory(
        work_name="Allowed wagon",
        department=Department.ZASVAR_1.value,
        type_wagon=TypeWagon.HAGAS.value,
    )
    disallowed = WorkFactory(
        work_name="Disallowed wagon",
        department=Department.MECHANIC.value,
        type_wagon=TypeWagon.HAGAS.value,
    )

    assert allowed.type_wagon == TypeWagon.HAGAS.value
    # MECHANIC isn't in ALLOWED_WAGON_DEPARTMENTS, so the explicit type_wagon
    # is silently dropped rather than rejected with a validation error.
    assert disallowed.type_wagon is None


@pytest.mark.django_db
def test_work_clean_rejects_duplicate_active_work_name_in_same_department():
    WorkFactory(department=Department.ZASVAR_1.value, work_name="Lathe")

    with pytest.raises(ValidationError):
        WorkFactory(department=Department.ZASVAR_1.value, work_name="Lathe")

    # Re-saving the original instance unchanged must not self-conflict.
    original = WorkFactory(department=Department.ZASVAR_1.value, work_name="Press")
    original.save()


@pytest.mark.django_db
def test_work_clean_allows_duplicate_work_name_when_existing_is_soft_deleted():
    WorkFactory(
        department=Department.ZASVAR_1.value,
        work_name="Drill press",
        is_deleted=True,
    )

    # The soft-deleted Work is excluded from the uniqueness check
    # (is_deleted=False filter), so a new active Work with the same
    # department/work_name is allowed.
    new_work = WorkFactory(
        department=Department.ZASVAR_1.value,
        work_name="Drill press",
        is_deleted=False,
    )

    assert new_work.pk is not None
