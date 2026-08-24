import pytest
from django.contrib.auth.models import Permission

from employee.constants.constants import Department
from employee.tests.factories import (
    DailySalaryFactory,
    DailyWorkFactory,
    EmployeeFactory,
    MasterFactory,
    PieceworkFactory,
    UserFactory,
    WorkFactory,
)

# Every change_* permission is seeded to Payrolls today, and Payrolls may browse
# any department - so these views line up with the boundary by coincidence of
# the seed. The editor below is the role that does not exist yet: allowed to
# edit, locked to one department. It keeps the two from drifting apart.

OTHER = Department.MECHANIC.value
OWN = Department.ZASVAR_1.value


def _locked_editor(codename):
    user = UserFactory()
    user.user_permissions.add(Permission.objects.get(codename=codename))
    MasterFactory(user=user, department=OWN)
    return user


def make_employee(department):
    return EmployeeFactory(department=department)


def make_work(department):
    return WorkFactory(department=department)


def make_daily_work(department):
    return DailyWorkFactory(work=WorkFactory(department=department))


def make_piecework(department):
    return PieceworkFactory(employee=EmployeeFactory(department=department))


def make_daily_salary(department):
    return DailySalaryFactory(employee=EmployeeFactory(department=department))


RENDERABLE_PAGES = [
    pytest.param(
        "change_employee", make_employee, "/employee_update/{pk}/", id="employee"
    ),
    pytest.param("change_work", make_work, "/work_update/{pk}/", id="work"),
    pytest.param(
        "change_dailywork", make_daily_work, "/daily_work_update/{pk}/", id="daily_work"
    ),
    pytest.param(
        "change_dailysalary",
        make_daily_salary,
        "/daily_salary_update/{pk}/",
        id="daily_salary",
    ),
]

# The piecework page cannot render at all: piecework/piecework_update.html was
# deleted in 2744c955 while the view and the route stayed, so a GET is a 500.
# The boundary below still has to hold - a 404 comes before any rendering.
PIECEWORK_PAGE = pytest.param(
    "change_piecework", make_piecework, "/piecework_update/{pk}/", id="piecework"
)

UPDATE_PAGES = [*RENDERABLE_PAGES, PIECEWORK_PAGE]


@pytest.mark.django_db
@pytest.mark.parametrize(("codename", "make_row", "url"), RENDERABLE_PAGES)
def test_the_update_view_opens_a_record_of_the_own_department(
    client, codename, make_row, url
):
    user = _locked_editor(codename)
    row = make_row(OWN)
    client.force_login(user)

    response = client.get(url.format(pk=row.pk))

    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(("codename", "make_row", "url"), UPDATE_PAGES)
def test_the_update_view_hides_a_record_of_another_department(
    client, codename, make_row, url
):
    user = _locked_editor(codename)
    row = make_row(OTHER)
    client.force_login(user)

    response = client.get(url.format(pk=row.pk))

    assert response.status_code == 404
