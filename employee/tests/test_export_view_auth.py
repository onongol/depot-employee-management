import pytest

from employee.constants.constants import GroupNames
from employee.tests.factories import UserFactory

# These 6 had no @login_required, so anyone with the URL could download full
# payroll/piecework/material data.
EXPORT_URLS_WITHOUT_EXTRA_PERMISSION = [
    "/daily_work_export_excel/",
    "/piecework_export_excel/",
    "/employee_salary_export_excel/",
    "/employee_salary_export_pdf/",
    "/wagon_export_excel/",
]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url", [*EXPORT_URLS_WITHOUT_EXTRA_PERMISSION, "/material_export_excel/"]
)
def test_export_view_redirects_anonymous_user(client, url):
    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize("url", EXPORT_URLS_WITHOUT_EXTRA_PERMISSION)
def test_export_view_allows_any_authenticated_user(client, url):
    # Only login required, matching their *_list siblings.
    user = UserFactory()
    client.force_login(user)

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_material_export_excel_forbids_authenticated_user_without_permission(client):
    # Unlike the other 5, its sibling material_list also requires this perm.
    user = UserFactory()
    client.force_login(user)

    response = client.get("/material_export_excel/")

    assert response.status_code == 403


@pytest.mark.django_db
def test_material_export_excel_allows_payrolls_group_member(client):
    user = UserFactory(groups=[GroupNames.PAYROLLS.value])
    client.force_login(user)

    response = client.get("/material_export_excel/")

    assert response.status_code == 200
