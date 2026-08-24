import pytest

from employee.tests.factories import UserFactory
from employee.views.daily_work.daily_work_prepare import daily_work_prepare
from employee.views.piecework.piecework_prepare import piecework_prepare

PREPARERS = [
    pytest.param(daily_work_prepare, "/daily_work/", id="daily_work"),
    pytest.param(piecework_prepare, "/piecework/", id="piecework"),
]


def _request(rf, path, user):
    request = rf.get(path)
    request.user = user
    request.session = {}
    return request


@pytest.mark.django_db
@pytest.mark.parametrize(("prepare", "path"), PREPARERS)
def test_a_non_ascii_digit_year_is_dropped(rf, prepare, path):
    # selected_year reaches filter(work_year=...), which int()s it. "²" passes
    # isdigit() but not int(), so it used to 500 under ?group=year.
    user = UserFactory()

    context = prepare(_request(rf, f"{path}?group=year&year=²", user))

    assert context.selected_year == ""


@pytest.mark.django_db
@pytest.mark.parametrize(("prepare", "path"), PREPARERS)
def test_an_ascii_digit_year_is_kept(rf, prepare, path):
    user = UserFactory()

    context = prepare(_request(rf, f"{path}?group=year&year=2024", user))

    assert context.selected_year == "2024"
