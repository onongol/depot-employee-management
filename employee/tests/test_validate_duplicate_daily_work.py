from datetime import date

import pytest

from employee.tests.factories import PieceworkFactory
from employee.views.daily_work.validators.validate_duplicate import validate_duplicate


@pytest.mark.django_db
def test_validate_duplicate_detects_matching_wagon_number():
    piecework = PieceworkFactory(work_date=date(2026, 3, 5), wagon_number="12")

    errors = validate_duplicate(
        selected_employee_ids=[piecework.employee_code],
        selected_work_ids=[piecework.work_id],
        work_date=piecework.work_date,
        type_work=piecework.type_work,
        wagon_number="12",
    )

    assert errors != []


@pytest.mark.django_db
def test_validate_duplicate_treats_empty_string_wagon_number_same_as_none():
    # The stored record has no wagon (None); normalize_str_field("") also
    # collapses to None, so passing "" must still be recognized as a match
    # against the isnull=True record rather than silently missing it.
    piecework = PieceworkFactory(work_date=date(2026, 3, 5), wagon_number=None)

    errors = validate_duplicate(
        selected_employee_ids=[piecework.employee_code],
        selected_work_ids=[piecework.work_id],
        work_date=piecework.work_date,
        type_work=piecework.type_work,
        wagon_number="",
    )

    assert errors != []


@pytest.mark.django_db
def test_validate_duplicate_skips_query_when_required_inputs_missing():
    errors = validate_duplicate(
        selected_employee_ids=[],
        selected_work_ids=[1],
        work_date=date(2026, 3, 5),
        type_work="84",
        wagon_number="12",
    )

    assert errors == []
