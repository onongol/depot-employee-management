from decimal import Decimal

import pytest

from employee.constants.constants import Department, GroupNames
from employee.tests.factories import (
    DailyWorkFactory,
    EmployeeFactory,
    MasterFactory,
    UserFactory,
    WorkFactory,
)
from employee.utils.request_department import get_selected_department_from_request
from employee.views.employee.employee_prepare import employee_prepare
from employee.views.employee_salary.employee_salary_prepare import (
    employee_salaries_prepare,
)
from employee.views.material.material_prepare import material_prepare
from employee.views.wagon.wagon_prepare import wagon_prepare
from employee.views.work.work_prepare import work_prepare

# One row per page that builds a department-scoped queryset. A new list without
# a boundary shows up here as a missing row, which is the point of the matrix.
# The pages whose base queryset filters on department unconditionally
# (daily_work, piecework, daily_salary) already come back empty without one.

OTHER = Department.MECHANIC.value
OWN = Department.ZASVAR_1.value


def make_employee(department):
    return EmployeeFactory(department=department)


def make_work(department):
    return WorkFactory(department=department)


def make_wagon_row(department):
    # The wagon report drops rows without a wagon before anything else.
    return DailyWorkFactory(work=WorkFactory(department=department), wagon_number="12")


def make_material_row(department):
    # The material report keeps only works that consume material.
    return DailyWorkFactory(
        work=WorkFactory(
            department=department,
            type_material="Steel sheet",
            usage_material=Decimal("1.0000"),
        )
    )


SCOPED_PAGES = [
    pytest.param(employee_prepare, "employees", make_employee, id="employees"),
    pytest.param(
        employee_salaries_prepare, "employees", make_employee, id="employee_salary"
    ),
    pytest.param(work_prepare, "works", make_work, id="works"),
    pytest.param(wagon_prepare, "daily_works", make_wagon_row, id="wagon"),
    pytest.param(material_prepare, "daily_works", make_material_row, id="material"),
]


def _rows(rf, user, prepare, attribute):
    request = rf.get("/")
    request.user = user
    request.session = {}
    get_selected_department_from_request(request)

    return list(getattr(prepare(request), attribute))


@pytest.mark.django_db
@pytest.mark.parametrize(("prepare", "attribute", "make_row"), SCOPED_PAGES)
def test_a_master_sees_only_their_own_department(rf, prepare, attribute, make_row):
    user = UserFactory(groups=[GroupNames.MASTERS.value])
    MasterFactory(user=user, department=OWN)
    own = make_row(OWN)
    make_row(OTHER)

    assert _rows(rf, user, prepare, attribute) == [own]


@pytest.mark.django_db
@pytest.mark.parametrize(("prepare", "attribute", "make_row"), SCOPED_PAGES)
def test_a_master_without_a_profile_sees_nothing(rf, prepare, attribute, make_row):
    user = UserFactory(groups=[GroupNames.MASTERS.value])
    make_row(OWN)
    make_row(OTHER)

    assert _rows(rf, user, prepare, attribute) == []


@pytest.mark.django_db
@pytest.mark.parametrize(("prepare", "attribute", "make_row"), SCOPED_PAGES)
def test_a_payroll_sees_every_department(rf, prepare, attribute, make_row):
    user = UserFactory(groups=[GroupNames.PAYROLLS.value])
    make_row(OWN)
    make_row(OTHER)

    assert len(_rows(rf, user, prepare, attribute)) == 2
