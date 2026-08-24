from employee.views.daily_salary.validators.validate_duplicate import (
    validate_daily_salary_duplicate,
)


def test_validate_daily_salary_duplicate_appends_error_when_duplicate_exists():
    errors = []

    result = validate_daily_salary_duplicate(
        emp_id=1,
        emp="Some Employee",
        existing_records={1, 2, 3},
        salary_date="2026-03-05",
        errors=errors,
    )

    assert len(errors) == 1
    # Must be truthy so the caller's `if validate_daily_salary_duplicate(...):
    # continue` in daily_salary_build_instances.py actually skips creating a
    # record for this employee.
    assert result is True


def test_validate_daily_salary_duplicate_returns_false_when_no_duplicate():
    errors = []

    result = validate_daily_salary_duplicate(
        emp_id=1,
        emp="Some Employee",
        existing_records={2, 3},
        salary_date="2026-03-05",
        errors=errors,
    )

    assert errors == []
    assert result is False
