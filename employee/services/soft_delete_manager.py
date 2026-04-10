from django.db import models

from employee.services.soft_delete_queryset import SoftDeleteQuerySet


class SoftDeleteManager(models.Manager):
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
        return self.all_with_deleted().dead()
