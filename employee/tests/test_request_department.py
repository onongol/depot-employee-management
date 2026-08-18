import pytest

from employee.constants.constants import Department, GroupNames
from employee.tests.factories import EmployeeFactory, MasterFactory, UserFactory
from employee.utils.request_department import get_selected_department_from_request


def _request(rf, user, department_param=None):
    url = (
        "/work/"
        if department_param is None
        else f"/work/?department={department_param}"
    )
    request = rf.get(url)
    request.user = user
    request.session = {}
    return request


@pytest.mark.django_db
def test_employee_is_locked_to_own_department_even_when_requesting_another(rf):
    user = UserFactory(groups=[GroupNames.EMPLOYEES.value])
    EmployeeFactory(user=user, department=Department.ZASVAR_1.value)

    request = _request(rf, user, department_param=Department.ZASVAR_2.value)

    assert get_selected_department_from_request(request) == Department.ZASVAR_1.value


@pytest.mark.django_db
def test_master_is_locked_to_own_department_even_when_requesting_another(rf):
    user = UserFactory(groups=[GroupNames.MASTERS.value])
    MasterFactory(user=user, department=Department.ZASVAR_1.value)

    request = _request(rf, user, department_param=Department.ZASVAR_2.value)

    assert get_selected_department_from_request(request) == Department.ZASVAR_1.value


@pytest.mark.django_db
def test_payrolls_can_pick_any_department(rf):
    user = UserFactory(groups=[GroupNames.PAYROLLS.value])

    request = _request(rf, user, department_param=Department.ZASVAR_2.value)

    assert get_selected_department_from_request(request) == Department.ZASVAR_2.value


@pytest.mark.django_db
def test_employee_without_linked_profile_gets_no_department(rf):
    # Safe fallback, not a leak: filters like department=None match nothing.
    user = UserFactory(groups=[GroupNames.EMPLOYEES.value])

    request = _request(rf, user, department_param=Department.ZASVAR_2.value)

    assert get_selected_department_from_request(request) is None
