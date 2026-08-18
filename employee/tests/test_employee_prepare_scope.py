import pytest

from employee.constants.constants import Department, GroupNames
from employee.tests.factories import EmployeeFactory, UserFactory
from employee.views.employee.employee_prepare import employee_prepare


def _request(rf, user):
    request = rf.get("/employee/")
    request.user = user
    request.session = {}
    return request


@pytest.mark.django_db
def test_user_without_view_employee_sees_only_own_record(rf):
    user = UserFactory(groups=[GroupNames.EMPLOYEES.value])
    own = EmployeeFactory(user=user, department=Department.ZASVAR_1.value)
    EmployeeFactory(department=Department.ZASVAR_1.value)

    context = employee_prepare(_request(rf, user))

    assert list(context.employees) == [own]


@pytest.mark.django_db
def test_masters_group_member_sees_every_record(rf):
    user = UserFactory(groups=[GroupNames.MASTERS.value])
    EmployeeFactory(department=Department.ZASVAR_1.value)
    EmployeeFactory(department=Department.ZASVAR_1.value)

    context = employee_prepare(_request(rf, user))

    assert context.employees.count() == 2


@pytest.mark.django_db
def test_superuser_without_any_group_sees_every_record(rf):
    user = UserFactory(is_superuser=True)
    EmployeeFactory(department=Department.ZASVAR_1.value)
    EmployeeFactory(department=Department.ZASVAR_1.value)

    context = employee_prepare(_request(rf, user))

    assert context.employees.count() == 2
