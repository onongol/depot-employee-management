from django.db import models


class SoftDeleteQuerySet(models.QuerySet):
    """QuerySet that supports soft deletion."""

    def delete(self):
        # One save() per row (not update()) so simple_history still fires.
        count = 0
        for obj in self:
            obj.delete()
            count += 1
        return count, {self.model._meta.label: count}

    # Keeps delete() off the manager, like Django's own QuerySet.delete does.
    delete.queryset_only = True

    def hard_delete(self):
        """Permanently delete every row in the queryset."""
        return super().delete()

    hard_delete.queryset_only = True

    def alive(self):
        return self.filter(is_deleted=False)

    def dead(self):
        return self.filter(is_deleted=True)
