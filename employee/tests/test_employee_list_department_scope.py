import pytest

from employee.constants.constants import Department, GroupNames
from employee.tests.factories import EmployeeFactory, MasterFactory, UserFactory
from employee.utils.filters.filter_employees import filter_employees
from employee.utils.request_department import get_selected_department_from_request
from employee.views.employee.employee_prepare import employee_prepare

# employee_prepare builds Employee.objects.all() without a department, unlike
# work_prepare and the rest - the department only ever gets applied by
# filter_employees. These two tests cover that single line from both sides.


def _list_for(rf, user):
    """The employee list pipeline: prepare, then the department guard.

    The department is resolved by UserContextCacheMiddleware in a real request,
    so the helper has to run it too - without it nothing is ever scoped.
    """
    request = rf.get("/employee/")
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
def test_a_master_without_a_linked_profile_sees_every_department(rf):
    # No Employee/Master row means get_user_department returns None, and a None
    # department switches the guard off entirely: "locked to your own
    # department" silently becomes "sees everyone".
    user = UserFactory(groups=[GroupNames.MASTERS.value])
    EmployeeFactory(department=Department.ZASVAR_1.value)
    EmployeeFactory(department=Department.MECHANIC.value)

    assert len(_list_for(rf, user)) == 2
