import pytest
from django.urls import reverse

from employee.constants.constants import Department, GroupNames
from employee.models import DailySalary, DailyWork, Employee, Work
from employee.tests.factories import (
    DailySalaryFactory,
    DailyWorkFactory,
    EmployeeFactory,
    PieceworkFactory,
    UserFactory,
    WorkFactory,
)

SELECTED = Department.ZASVAR_1.value
OTHER = Department.ZASVAR_2.value


def _work(department):
    return WorkFactory(department=department)


def _employee(department):
    return EmployeeFactory(department=department)


def _daily_work(department):
    # DailyWork snapshots department from its Work.
    return DailyWorkFactory(work=WorkFactory(department=department))


def _daily_salary(department):
    # DailySalary snapshots department from its Employee.
    return DailySalaryFactory(employee=EmployeeFactory(department=department))


# Every destructive bulk endpoint, with the POST field its template posts.
DELETE_BULK_VIEWS = [
    pytest.param("work_delete_bulk", "work_table_ids", _work, Work, id="work"),
    pytest.param(
        "employee_delete_bulk",
        "employee_table_ids",
        _employee,
        Employee,
        id="employee",
    ),
    pytest.param(
        "daily_work_delete_bulk",
        "daily_work_ids",
        _daily_work,
        DailyWork,
        id="daily_work",
    ),
    pytest.param(
        "daily_salary_delete_bulk",
        "daily_salary_ids",
        _daily_salary,
        DailySalary,
        id="daily_salary",
    ),
]


def _login_with_department(client, department, groups=(GroupNames.PAYROLLS.value,)):
    """Log in and pick a department the way the real request cycle does.

    Payrolls holds all four delete_* permissions plus select_department. The
    session has to be written after force_login: logging in fires
    set_department_on_login, which would overwrite it.
    """
    user = UserFactory(groups=list(groups))
    client.force_login(user)
    session = client.session
    session["department"] = department
    session.save()
    return user


@pytest.mark.django_db
@pytest.mark.parametrize("url_name, post_field, make_row, model", DELETE_BULK_VIEWS)
def test_delete_bulk_does_not_touch_another_department(
    client, url_name, post_field, make_row, model
):
    # The department kwarg on the queryset is the entire security boundary:
    # the ids are attacker-controlled POST data, the department is not. On a
    # POST request.GET is empty, so it can only come from the session.
    _login_with_department(client, SELECTED)
    row = make_row(OTHER)

    client.post(reverse(url_name), {post_field: [row.pk]})

    assert model.objects.filter(pk=row.pk).exists()


@pytest.mark.django_db
@pytest.mark.parametrize("url_name, post_field, make_row, model", DELETE_BULK_VIEWS)
def test_delete_bulk_deletes_rows_of_the_selected_department(
    client, url_name, post_field, make_row, model
):
    # Control for the test above: without this one, a view that silently
    # deleted nothing at all would look perfectly secure.
    _login_with_department(client, SELECTED)
    row = make_row(SELECTED)

    client.post(reverse(url_name), {post_field: [row.pk]})

    assert not model.objects.filter(pk=row.pk).exists()


@pytest.mark.django_db
@pytest.mark.parametrize("url_name, post_field, make_row, model", DELETE_BULK_VIEWS)
def test_delete_bulk_with_unparsable_ids_deletes_nothing(
    client, url_name, post_field, make_row, model
):
    # parse_ids drops everything here, and an empty id list must mean "nothing
    # selected", never "no filter".
    _login_with_department(client, SELECTED)
    row = make_row(SELECTED)

    client.post(reverse(url_name), {post_field: ["abc", ""]})

    assert model.objects.filter(pk=row.pk).exists()


@pytest.mark.django_db
@pytest.mark.parametrize("url_name, post_field, make_row, model", DELETE_BULK_VIEWS)
def test_delete_bulk_rejects_a_user_without_the_delete_permission(
    client, url_name, post_field, make_row, model
):
    _login_with_department(client, SELECTED, groups=[GroupNames.MASTERS.value])
    row = make_row(SELECTED)

    client.post(reverse(url_name), {post_field: [row.pk]})

    assert model.objects.filter(pk=row.pk).exists()


@pytest.mark.django_db
@pytest.mark.parametrize("url_name, post_field, make_row, model", DELETE_BULK_VIEWS)
def test_delete_bulk_rejects_an_anonymous_user(
    client, url_name, post_field, make_row, model
):
    row = make_row(SELECTED)

    response = client.post(reverse(url_name), {post_field: [row.pk]})

    assert response.status_code == 302
    assert model.objects.filter(pk=row.pk).exists()


@pytest.mark.django_db
def test_employee_delete_bulk_keeps_an_employee_that_has_piecework(client):
    _login_with_department(client, SELECTED)
    employee = EmployeeFactory(department=SELECTED)
    PieceworkFactory(employee=employee)

    client.post(reverse("employee_delete_bulk"), {"employee_table_ids": [employee.pk]})

    assert Employee.objects.filter(pk=employee.pk).exists()


@pytest.mark.django_db
def test_employee_delete_bulk_deletes_an_employee_without_piecework(client):
    # Pins the blocked/deletable split itself: if has_piecework stopped being
    # annotated, every row would land in one bucket and only one of these two
    # tests would notice.
    _login_with_department(client, SELECTED)
    employee = EmployeeFactory(department=SELECTED)

    client.post(reverse("employee_delete_bulk"), {"employee_table_ids": [employee.pk]})

    assert not Employee.objects.filter(pk=employee.pk).exists()


@pytest.mark.django_db
def test_daily_salary_delete_bulk_keeps_a_record_with_matching_piecework(client):
    # Blocked only when employee, employee_code and the date all line up —
    # this is the piecework that was actually paid for that salary day.
    _login_with_department(client, SELECTED)
    employee = EmployeeFactory(department=SELECTED)
    daily_salary = DailySalaryFactory(employee=employee)
    PieceworkFactory(employee=employee, work_date=daily_salary.salary_date)

    client.post(
        reverse("daily_salary_delete_bulk"), {"daily_salary_ids": [daily_salary.pk]}
    )

    assert DailySalary.objects.filter(pk=daily_salary.pk).exists()
