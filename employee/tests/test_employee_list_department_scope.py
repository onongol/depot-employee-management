import pytest

from employee.constants.constants import Department, GroupNames
from employee.tests.factories import EmployeeFactory, MasterFactory, UserFactory
from employee.utils.filters.filter_employees import filter_employees
from employee.utils.request_department import get_selected_department_from_request
from employee.views.employee.employee_prepare import employee_prepare

# The list has two layers and they are not interchangeable: Employee.objects
# .for_user() is the boundary (what the user may reach at all), the department
# in the context is the one they picked in the UI. These tests run both.


def _list_for(rf, user, department=None):
    """The employee list pipeline: prepare, then the picked-department filter.

    The department is resolved by UserContextCacheMiddleware in a real request,
    so the helper has to run it too.
    """
    query = {"department": department} if department else {}
    request = rf.get("/employee/", query)
    request.user = user
    request.session = {}
    get_selected_department_from_request(request)

    context = employee_prepare(request)
    return list(filter_employees(context.employees, context=context))


@pytest.mark.django_db
def test_a_master_only_sees_the_employees_of_their_own_department(rf):
    user = UserFactory(groups=[GroupNames.MASTERS.value])
    MasterFactory(user=user, department=Department.ZASVAR_1.value)
    own_department = EmployeeFactory(department=Department.ZASVAR_1.value)
    EmployeeFactory(department=Department.MECHANIC.value)

    assert _list_for(rf, user) == [own_department]


@pytest.mark.django_db
def test_a_master_without_a_linked_profile_sees_nothing(rf):
    # No Employee/Master row means no department, and for_user fails closed:
    # before it existed, a missing profile turned "locked to your own
    # department" into "sees everyone".
    user = UserFactory(groups=[GroupNames.MASTERS.value])
    EmployeeFactory(department=Department.ZASVAR_1.value)
    EmployeeFactory(department=Department.MECHANIC.value)

    assert _list_for(rf, user) == []


@pytest.mark.django_db
def test_a_payroll_sees_every_department_until_one_is_picked(rf):
    # "All departments" is a consequence of select_department, not of an unset
    # value - that is the whole point of the boundary.
    user = UserFactory(groups=[GroupNames.PAYROLLS.value])
    zasvar = EmployeeFactory(department=Department.ZASVAR_1.value)
    EmployeeFactory(department=Department.MECHANIC.value)

    assert len(_list_for(rf, user)) == 2
    assert _list_for(rf, user, department=Department.ZASVAR_1.value) == [zasvar]
