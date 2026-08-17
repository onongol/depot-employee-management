from decimal import Decimal

import pytest

from employee.constants.constants import Department
from employee.tests.factories import EmployeeFactory, PieceworkFactory, WorkFactory


@pytest.mark.django_db
def test_piecework_save_generates_group_id_once_and_keeps_it_stable():
    piecework = PieceworkFactory()

    group_id = piecework.group_id
    assert group_id  # a uuid was generated since none was given

    # Re-saving (e.g. sync_single_piecework does this on every DailyWork edit)
    # must not mint a new group_id — it identifies the original batch.
    piecework.amount = Decimal("9.00")
    piecework.save()

    assert piecework.group_id == group_id


@pytest.mark.django_db
def test_piecework_save_keeps_an_explicitly_provided_group_id():
    # piecework_create_bulk assigns the same group_id to every Piecework in a
    # batch so they can be managed together; save() must not override that.
    piecework = PieceworkFactory(group_id="batch-123")

    assert piecework.group_id == "batch-123"


@pytest.mark.django_db
def test_piecework_save_snapshots_department_from_employee_not_work_and_updates_on_resave():
    employee = EmployeeFactory(
        employee_name="Original Name", department=Department.ZASVAR_1.value
    )
    work = WorkFactory(work_name="Original Work", department=Department.ZASVAR_2.value)

    piecework = PieceworkFactory(employee=employee, work=work)

    assert piecework.employee_code == employee.employee_id
    assert piecework.employee_name == "Original Name"
    # department is a snapshot of the employee's department, not the work's
    # (DailyWork snapshots department from Work instead — an asymmetry
    # between the two sibling models).
    assert piecework.department == Department.ZASVAR_1.value
    assert piecework.work_name == "Original Work"

    employee.employee_name = "Renamed Employee"
    employee.department = Department.HOS_DUGUI.value
    employee.save()
    work.work_name = "Renamed Work"
    work.save()

    piecework.save()

    assert piecework.employee_name == "Renamed Employee"
    assert piecework.department == Department.HOS_DUGUI.value
    assert piecework.work_name == "Renamed Work"
