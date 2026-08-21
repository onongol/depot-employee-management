import pytest

from employee.models import Employee, Master, Payroll, Work
from employee.tests.factories import (
    EmployeeFactory,
    MasterFactory,
    PayrollFactory,
    UserFactory,
    WorkFactory,
)

# Every model wired to SoftDeleteManager/SoftDeleteQuerySet. The whole app
# leans on this: list views, exports and totals all read through `objects` and
# assume it hides deleted rows, while `all_objects` is what bulk delete and the
# admin changelist use to still see them.
SOFT_DELETE_MODELS = [
    pytest.param(EmployeeFactory, Employee, id="Employee"),
    pytest.param(MasterFactory, Master, id="Master"),
    pytest.param(PayrollFactory, Payroll, id="Payroll"),
    pytest.param(WorkFactory, Work, id="Work"),
]

# The three that carry a linked User. Work has no login attached to it.
PROFILE_FACTORIES = [
    pytest.param(EmployeeFactory, id="Employee"),
    pytest.param(MasterFactory, id="Master"),
    pytest.param(PayrollFactory, id="Payroll"),
]


@pytest.mark.django_db
@pytest.mark.parametrize("factory, model", SOFT_DELETE_MODELS)
def test_objects_hides_deleted_rows_and_all_objects_shows_them(factory, model):
    alive = factory()
    deleted = factory(is_deleted=True)

    assert list(model.objects.filter(pk__in=[alive.pk, deleted.pk])) == [alive]
    assert model.all_objects.filter(pk__in=[alive.pk, deleted.pk]).count() == 2


@pytest.mark.django_db
@pytest.mark.parametrize("factory, model", SOFT_DELETE_MODELS)
def test_delete_keeps_the_row_in_the_database(factory, model):
    obj = factory()

    obj.delete()

    assert model.objects.filter(pk=obj.pk).count() == 0
    assert model.all_objects.get(pk=obj.pk).is_deleted is True


@pytest.mark.django_db
@pytest.mark.parametrize("factory, model", SOFT_DELETE_MODELS)
def test_restore_brings_a_deleted_row_back(factory, model):
    obj = factory()
    obj.delete()

    obj.restore()

    assert model.objects.filter(pk=obj.pk).count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize("factory, model", SOFT_DELETE_MODELS)
def test_hard_delete_really_removes_the_row(factory, model):
    obj = factory()

    obj.hard_delete()

    assert model.all_objects.filter(pk=obj.pk).count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize("factory, model", SOFT_DELETE_MODELS)
def test_queryset_exposes_the_alive_and_dead_filters(factory, model):
    # These only exist if the manager actually hands out a SoftDeleteQuerySet.
    alive = factory()
    deleted = factory(is_deleted=True)

    assert list(model.all_objects.all().alive()) == [alive]
    assert list(model.all_objects.all().dead()) == [deleted]


@pytest.mark.django_db
@pytest.mark.parametrize("factory, model", SOFT_DELETE_MODELS)
def test_queryset_delete_is_soft_like_instance_delete(factory, model):
    # The one that matters: deleting through a queryset must not be a harder
    # delete than deleting the same row through the instance. Anyone folding
    # the per-object loops in admin_log_delete.py / SoftDeleteAdminMixin into
    # a single queryset.delete() has to land here, not in lost data.
    obj = factory()

    model.objects.filter(pk=obj.pk).delete()

    assert model.all_objects.get(pk=obj.pk).is_deleted is True
    assert model.objects.filter(pk=obj.pk).count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize("factory, model", SOFT_DELETE_MODELS)
def test_delete_is_not_reachable_from_the_manager(factory, model):
    # Manager.from_queryset() copies every public queryset method onto the
    # manager unless it is flagged queryset_only, which is why Django flags its
    # own QuerySet.delete. Without that flag on ours, `Model.objects.delete()`
    # would exist and wipe the table in one argument-less call.
    assert not hasattr(model.objects, "delete")
    assert not hasattr(model.objects, "hard_delete")


@pytest.mark.django_db
@pytest.mark.parametrize("factory", PROFILE_FACTORIES)
def test_delete_deactivates_the_linked_user(factory):
    # Otherwise a deleted profile leaves a working login behind: the person
    # still authenticates, they just land in an app with no data.
    linked_user = UserFactory(is_active=True)
    profile = factory(user=linked_user)

    profile.delete()

    linked_user.refresh_from_db()
    assert linked_user.is_active is False


@pytest.mark.django_db
@pytest.mark.parametrize("factory", PROFILE_FACTORIES)
def test_restore_reactivates_the_linked_user(factory):
    linked_user = UserFactory(is_active=True)
    profile = factory(user=linked_user)
    profile.delete()

    profile.restore()

    linked_user.refresh_from_db()
    assert linked_user.is_active is True


@pytest.mark.django_db
@pytest.mark.parametrize("factory", PROFILE_FACTORIES)
def test_delete_does_not_reactivate_an_already_inactive_user(factory):
    # is_active=False must survive the delete/restore round trip.
    linked_user = UserFactory(is_active=True)
    profile = factory(user=linked_user, is_active=False)
    profile.delete()

    profile.restore()

    linked_user.refresh_from_db()
    assert linked_user.is_active is False


@pytest.mark.django_db
@pytest.mark.parametrize("factory, model", SOFT_DELETE_MODELS)
def test_delete_and_restore_are_written_to_history(factory, model):
    # The audit trail is the reason soft delete goes through save() per object:
    # a bulk update(is_deleted=True) never fires post_save, so simple_history
    # would record nothing and update_change_reason would have no row to tag.
    obj = factory()

    obj.delete()

    assert obj.history.first().history_change_reason == "Soft deleted"

    obj.restore()

    assert obj.history.first().history_change_reason == "Restored"
