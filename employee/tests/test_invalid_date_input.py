import pytest

from employee.forms.filter_forms import SalaryDateForm
from employee.models import DailyWork
from employee.tests.factories import (
    DailySalaryFactory,
    DailyWorkFactory,
    EmployeeFactory,
)
from employee.utils.filters.filter_daily_works import filter_daily_works
from employee.views.daily_salary.daily_salary_create.daily_salary_create_service import (
    create_daily_salary_records,
)
from employee.views.daily_work.daily_work_create.daily_work_create_prepare import (
    daily_work_piecework_create_prepare,
)
from employee.views.daily_work.daily_work_prepare import daily_work_prepare

# Flatpickr runs with allowInput, so a user can type any of these into the box.
UNPARSABLE = ["22.08.2026", "2026-02-30", "garbage"]


def _request(rf, path):
    request = rf.get(path)
    request.session = {}
    return request


@pytest.mark.django_db
@pytest.mark.parametrize("record_date", UNPARSABLE)
def test_an_unparsable_record_date_does_not_reach_the_orm(rf, record_date):
    # A raw string in filter(record_date__date=...) raises ValidationError at
    # filter() time, which is a 500 on a page a user can reach by typing.
    DailyWorkFactory()
    context = daily_work_prepare(
        _request(rf, f"/daily_work/?record_date={record_date}")
    )

    result = filter_daily_works(DailyWork.objects.all(), context=context)

    assert result.count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize("work_date", UNPARSABLE)
def test_an_unparsable_work_date_falls_back_to_today(rf, work_date):
    # Not None: work_date=None is SQL IS NULL, which empties existing_pieceworks
    # and silently turns the duplicate check off.
    context = daily_work_piecework_create_prepare(
        _request(rf, f"/daily_work/create/?work_date={work_date}")
    )

    assert context.work_date == context.today


@pytest.mark.django_db
@pytest.mark.parametrize("salary_date", UNPARSABLE)
def test_an_unparsable_salary_date_is_an_error_not_a_crash(salary_date):
    employee = EmployeeFactory()
    DailySalaryFactory(employee=employee)

    parsed = SalaryDateForm.parse({"salary_date": salary_date}).get("salary_date")
    employees_dict, errors = create_daily_salary_records(
        [employee.employee_id], parsed, hours_per_day=8
    )

    assert employees_dict is None
    assert errors
