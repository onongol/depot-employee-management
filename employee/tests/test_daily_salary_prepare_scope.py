import pytest

from employee.constants.constants import Department, GroupNames
from employee.tests.factories import (
    DailySalaryFactory,
    EmployeeFactory,
    UserFactory,
)
from employee.views.daily_salary.daily_salary_prepare import daily_salary_prepare


def _request(rf, user, department):
    request = rf.get(f"/daily-salary/?department={department}")
    request.user = user
    request.session = {}
    return request


@pytest.mark.django_db
def test_user_without_view_dailysalary_sees_only_own_records(rf):
    department = Department.ZASVAR_1.value
    user = UserFactory(groups=[GroupNames.EMPLOYEES.value])
    own_employee = EmployeeFactory(user=user, department=department)
    own = DailySalaryFactory(employee=own_employee, department=department)
    DailySalaryFactory(
        employee=EmployeeFactory(department=department), department=department
    )

    context = daily_salary_prepare(_request(rf, user, department))

    assert list(context.daily_salaries) == [own]


@pytest.mark.django_db
def test_masters_group_member_sees_every_record(rf):
    department = Department.ZASVAR_1.value
    user = UserFactory(groups=[GroupNames.MASTERS.value])
    for _ in range(2):
        DailySalaryFactory(
            employee=EmployeeFactory(department=department), department=department
        )

    context = daily_salary_prepare(_request(rf, user, department))

    assert context.daily_salaries.count() == 2
