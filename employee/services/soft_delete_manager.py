from django.db import models

from employee.services.soft_delete_queryset import SoftDeleteQuerySet


class SoftDeleteManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    """Manager that filters out soft-deleted records by default.

    from_queryset() wires up SoftDeleteQuerySet; without it queryset .delete()
    was a plain hard delete.
    """

    def __init__(self, *args, only_alive=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.only_alive = only_alive

    def get_queryset(self):
        qs = super().get_queryset()
        if self.only_alive:
            return qs.filter(is_deleted=False)
        return qs

    def all_with_deleted(self):
        return SoftDeleteQuerySet(self.model, using=self._db)

    def dead(self):
        # Must override: the copied dead() would go through get_queryset()
        # and always come back empty.
        return self.all_with_deleted().dead()
