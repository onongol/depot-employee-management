import pytest

from employee.constants.constants import GroupNames
from employee.tests.factories import UserFactory, WorkFactory


@pytest.mark.django_db
def test_work_update_view_redirects_anonymous_user(client):
    work = WorkFactory()

    response = client.get(f"/work_update/{work.pk}/")

    assert response.status_code == 302


@pytest.mark.django_db
def test_work_update_view_forbids_authenticated_user_without_permission(client):
    # PermissionRequiredMixin/UserPassesTestMixin both use AccessMixin's
    # handle_no_permission(), which only redirects an ANONYMOUS user — an
    # already-authenticated user lacking the permission gets a 403 instead.
    # Same behavior OnlyPayrollsMixin had before this migration.
    work = WorkFactory()
    user = UserFactory()  # no permission
    client.force_login(user)

    response = client.get(f"/work_update/{work.pk}/")

    assert response.status_code == 403


@pytest.mark.django_db
def test_work_update_view_allows_payrolls_group_member(client):
    work = WorkFactory()
    user = UserFactory(groups=[GroupNames.PAYROLLS.value])
    client.force_login(user)

    response = client.get(f"/work_update/{work.pk}/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_material_list_view_redirects_authenticated_user_without_permission(client):
    # permission_required is a thin wrapper over user_passes_test, which
    # (unlike AccessMixin/PermissionRequiredMixin on the CBV side) always
    # redirects on failure regardless of authentication status — never a 403.
    user = UserFactory()  # no permission
    client.force_login(user)

    response = client.get("/material/")

    assert response.status_code == 302


@pytest.mark.django_db
def test_material_list_view_allows_payrolls_group_member(client):
    user = UserFactory(groups=[GroupNames.PAYROLLS.value])
    client.force_login(user)

    response = client.get("/material/")

    assert response.status_code == 200
