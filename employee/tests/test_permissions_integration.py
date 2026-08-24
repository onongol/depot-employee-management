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
def test_material_list_view_forbids_authenticated_user_without_permission(client):
    # Without raise_exception=True, permission_required redirects to LOGIN_URL
    # even for an authenticated user, and allauth bounces them straight back
    # via ?next= — an infinite redirect loop instead of a 403.
    user = UserFactory()  # no permission
    client.force_login(user)

    response = client.get("/material/")

    assert response.status_code == 403


@pytest.mark.django_db
def test_material_list_view_does_not_loop_for_masters_group_member(client):
    # Masters lack view_material_report. follow=True raises RedirectCycleError
    # if the login redirect ever comes back — the regression this guards.
    user = UserFactory(groups=[GroupNames.MASTERS.value])
    client.force_login(user)

    response = client.get("/material/", follow=True)

    assert response.status_code == 403
    assert response.redirect_chain == []


@pytest.mark.django_db
def test_material_list_view_still_redirects_anonymous_user(client):
    # raise_exception=True would 403 anonymous users too; @login_required sits
    # above the decorator and must keep catching them first.
    response = client.get("/material/")

    assert response.status_code == 302
    assert "/accounts/login/" in response.headers["Location"]


@pytest.mark.django_db
def test_material_list_view_allows_payrolls_group_member(client):
    user = UserFactory(groups=[GroupNames.PAYROLLS.value])
    client.force_login(user)

    response = client.get("/material/")

    assert response.status_code == 200
