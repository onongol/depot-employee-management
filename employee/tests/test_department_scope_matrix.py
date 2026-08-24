from decimal import Decimal

import pytest

from employee.constants.constants import Department, GroupNames
from employee.tests.factories import (
    DailySalaryFactory,
    DailyWorkFactory,
    EmployeeFactory,
    MasterFactory,
    PieceworkFactory,
    UserFactory,
    WorkFactory,
)
from employee.utils.request_department import get_selected_department_from_request
from employee.views.daily_salary.daily_salary_prepare import daily_salary_prepare
from employee.views.daily_work.daily_work_prepare import daily_work_prepare
from employee.views.employee.employee_prepare import employee_prepare
from employee.views.employee_salary.employee_salary_prepare import (
    employee_salaries_prepare,
)
from employee.views.material.material_prepare import material_prepare
from employee.views.piecework.piecework_prepare import piecework_prepare
from employee.views.wagon.wagon_prepare import wagon_prepare
from employee.views.work.work_prepare import work_prepare

# One row per page in PAGES_REQUIRING_DEPARTMENT (see the department_warning
# context processor). All seven answer the same way now: for_user() is the
# boundary, the picked department is mandatory, and no department means no
# rows - which is what the warning banner has been telling users all along.
# A new list without a boundary shows up here as a missing row.

OTHER = Department.MECHANIC.value
OWN = Department.ZASVAR_1.value


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
    pytest.param(daily_work_prepare, "daily_works", make_daily_work, id="daily_work"),
    pytest.param(piecework_prepare, "pieceworks", make_piecework, id="piecework"),
    pytest.param(
        daily_salary_prepare, "daily_salaries", make_daily_salary, id="daily_salary"
    ),
]


def _rows(rf, user, prepare, attribute, department=None):
    query = {"department": department} if department else {}
    request = rf.get("/", query)
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
def test_a_payroll_sees_nothing_until_a_department_is_picked(
    rf, prepare, attribute, make_row
):
    # May browse every department, but not all of them at once: an unpicked
    # department is not "everything", it is "not chosen yet".
    user = UserFactory(groups=[GroupNames.PAYROLLS.value])
    make_row(OWN)
    make_row(OTHER)

    assert _rows(rf, user, prepare, attribute) == []


@pytest.mark.django_db
@pytest.mark.parametrize(("prepare", "attribute", "make_row"), SCOPED_PAGES)
def test_a_payroll_sees_the_department_they_picked(rf, prepare, attribute, make_row):
    user = UserFactory(groups=[GroupNames.PAYROLLS.value])
    own = make_row(OWN)
    make_row(OTHER)

    assert _rows(rf, user, prepare, attribute, department=OWN) == [own]


# --- material: plant-wide by design -----------------------------------------
# material_list is deliberately absent from PAGES_REQUIRING_DEPARTMENT and its
# filter panel has no department field, so the report spans the whole depot.
# The boundary still applies.


@pytest.mark.django_db
def test_the_material_report_spans_every_department_for_a_payroll(rf):
    user = UserFactory(groups=[GroupNames.PAYROLLS.value])
    make_material_row(OWN)
    make_material_row(OTHER)

    assert len(_rows(rf, user, material_prepare, "daily_works")) == 2


@pytest.mark.django_db
def test_the_material_report_is_empty_without_a_department(rf):
    user = UserFactory(groups=[GroupNames.MASTERS.value])
    make_material_row(OWN)
    make_material_row(OTHER)

    assert _rows(rf, user, material_prepare, "daily_works") == []
