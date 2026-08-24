import pytest
from django.contrib.auth.models import Permission

from employee.constants.constants import Department, GroupNames
from employee.models import Employee
from employee.tests.factories import EmployeeFactory, MasterFactory, UserFactory

# for_user() itself, plus the activate/deactivate action - the update views of
# every model live in test_update_view_department_scope.py.


def _department_locked_editor(*codenames):
    """A user who may edit employees but may not leave their own department."""
    user = UserFactory()
    user.user_permissions.add(
        *Permission.objects.filter(codename__in=codenames),
    )
    MasterFactory(user=user, department=Department.ZASVAR_1.value)
    return user


# --- the queryset method itself ---------------------------------------------


@pytest.mark.django_db
def test_for_user_returns_every_department_with_select_department():
    user = UserFactory(groups=[GroupNames.PAYROLLS.value])
    EmployeeFactory(department=Department.ZASVAR_1.value)
    EmployeeFactory(department=Department.MECHANIC.value)

    assert Employee.objects.for_user(user).count() == 2


@pytest.mark.django_db
def test_for_user_returns_only_the_own_department_without_the_permission():
    user = UserFactory()
    MasterFactory(user=user, department=Department.ZASVAR_1.value)
    own_department = EmployeeFactory(department=Department.ZASVAR_1.value)
    EmployeeFactory(department=Department.MECHANIC.value)

    assert list(Employee.objects.for_user(user)) == [own_department]


@pytest.mark.django_db
def test_for_user_returns_nothing_without_a_department():
    user = UserFactory()
    EmployeeFactory(department=Department.ZASVAR_1.value)

    assert list(Employee.objects.for_user(user)) == []


# --- the views that take a pk -----------------------------------------------


@pytest.mark.django_db
def test_the_deactivate_action_still_works_inside_the_own_department(client):
    user = _department_locked_editor("change_employee_status")
    employee = EmployeeFactory(department=Department.ZASVAR_1.value, is_active=True)
    client.force_login(user)

    response = client.get(f"/employee/{employee.pk}/deactivate/")

    assert response.status_code == 302
    employee.refresh_from_db()
    assert employee.is_active is False


@pytest.mark.django_db
def test_the_deactivate_action_hides_an_employee_of_another_department(client):
    user = _department_locked_editor("change_employee_status")
    employee = EmployeeFactory(department=Department.MECHANIC.value, is_active=True)
    client.force_login(user)

    response = client.get(f"/employee/{employee.pk}/deactivate/")

    assert response.status_code == 404
    employee.refresh_from_db()
    assert employee.is_active is True
