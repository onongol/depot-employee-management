import pytest

from employee.constants.constants import Department, GroupNames
from employee.tests.factories import EmployeeFactory, MasterFactory, UserFactory
from employee.utils.request_department import get_selected_department_from_request
from employee.views.employee.employee_prepare import employee_prepare


def _request(rf, user, department=None):
    """A request as the middleware leaves it: department already resolved."""
    query = {"department": department} if department else {}
    request = rf.get("/employee/", query)
    request.user = user
    request.session = {}
    get_selected_department_from_request(request)
    return request


@pytest.mark.django_db
def test_user_without_view_employee_sees_only_own_record(rf):
    user = UserFactory(groups=[GroupNames.EMPLOYEES.value])
    own = EmployeeFactory(user=user, department=Department.ZASVAR_1.value)
    EmployeeFactory(department=Department.ZASVAR_1.value)

    context = employee_prepare(_request(rf, user))

    assert list(context.employees) == [own]


@pytest.mark.django_db
def test_masters_group_member_sees_every_record_of_their_department(rf):
    user = UserFactory(groups=[GroupNames.MASTERS.value])
    MasterFactory(user=user, department=Department.ZASVAR_1.value)
    EmployeeFactory(department=Department.ZASVAR_1.value)
    EmployeeFactory(department=Department.ZASVAR_1.value)

    context = employee_prepare(_request(rf, user))

    assert context.employees.count() == 2


@pytest.mark.django_db
def test_superuser_without_any_group_sees_every_record_of_the_picked_department(rf):
    # A superuser has select_department, so the department still has to be
    # picked - it just is not forced to be their own.
    user = UserFactory(is_superuser=True)
    EmployeeFactory(department=Department.ZASVAR_1.value)
    EmployeeFactory(department=Department.ZASVAR_1.value)

    context = employee_prepare(_request(rf, user, department=Department.ZASVAR_1.value))

    assert context.employees.count() == 2
