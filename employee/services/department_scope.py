from django.db import models

from employee.services.soft_delete_manager import SoftDeleteManager
from employee.services.soft_delete_queryset import SoftDeleteQuerySet


class DepartmentScopedQuerySet(models.QuerySet):
    """for_user(): the department boundary, shared by every scoped model."""

    def for_user(self, user):
        """Fails closed: no department (no perm, no linked profile) means no rows.
        This is the hard boundary; a privileged user's UI department pick is a separate filter on top.
        """
        from employee.utils.request_department import get_user_department

        if user.has_perm("employee.select_department"):
            return self

        department = get_user_department(user)
        if not department:
            return self.none()
        return self.filter(department=department)


class DepartmentScopedManager(models.Manager.from_queryset(DepartmentScopedQuerySet)):
    """Default manager for scoped models without soft delete."""


class ScopedSoftDeleteQuerySet(DepartmentScopedQuerySet, SoftDeleteQuerySet):
    """Both mixins for the models that are soft-deletable and scoped."""


class ScopedSoftDeleteManager(
    SoftDeleteManager.from_queryset(ScopedSoftDeleteQuerySet)
):
    """SoftDeleteManager with for_user() on top."""
