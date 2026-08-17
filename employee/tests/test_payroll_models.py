import pytest
from django.core.exceptions import ValidationError

from employee.tests.factories import PayrollFactory


@pytest.mark.django_db
def test_payroll_clean_rejects_duplicate_active_payroll_id():
    PayrollFactory(payroll_id=42)

    duplicate = PayrollFactory.build(payroll_id=42)
    with pytest.raises(ValidationError):
        duplicate.full_clean()

    original = PayrollFactory(payroll_id=99)
    original.full_clean()


@pytest.mark.django_db
def test_payroll_clean_allows_duplicate_payroll_id_when_existing_is_soft_deleted():
    PayrollFactory(payroll_id=42, is_deleted=True)

    new_payroll = PayrollFactory.build(payroll_id=42, is_deleted=False)

    new_payroll.full_clean()  # must not raise


@pytest.mark.django_db
def test_payroll_save_uniqueness():
    PayrollFactory(payroll_id=42)

    with pytest.raises(ValidationError):
        PayrollFactory(payroll_id=42)
