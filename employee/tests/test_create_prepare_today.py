from datetime import UTC, date, datetime

import pytest

from employee.views.daily_salary.daily_salary_create.daily_salary_create_prepare import (
    prepare_daily_salary_create,
)
from employee.views.daily_work.daily_work_create.daily_work_create_prepare import (
    daily_work_piecework_create_prepare,
)

# 03:00 in Asia/Ulaanbaatar (UTC+8). now().date() would call this 2026-08-22.
EARLY_MORNING_UTC = datetime(2026, 8, 22, 19, 0, tzinfo=UTC)
LOCAL_DAY = date(2026, 8, 23)


@pytest.fixture
def _early_morning(monkeypatch):
    monkeypatch.setattr(
        "django.utils.timezone.now", lambda: EARLY_MORNING_UTC, raising=True
    )


def _request(rf, path):
    request = rf.get(path)
    request.session = {}
    return request


@pytest.mark.django_db
@pytest.mark.usefixtures("_early_morning")
def test_daily_work_create_defaults_to_the_local_day(rf):
    context = daily_work_piecework_create_prepare(_request(rf, "/daily-work/create/"))

    assert context.today == LOCAL_DAY
    assert context.work_date == LOCAL_DAY


@pytest.mark.django_db
@pytest.mark.usefixtures("_early_morning")
def test_daily_salary_create_defaults_to_the_local_day(rf):
    context = prepare_daily_salary_create(_request(rf, "/daily-salary/create/"))

    assert context.today == LOCAL_DAY
