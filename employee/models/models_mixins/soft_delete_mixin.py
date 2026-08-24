from django.db import transaction
from simple_history.utils import update_change_reason


class SoftDeleteMixin:
    """Mixin providing soft delete, restore, and hard delete for models."""

    def delete(self, using=None, keep_parents=False):
        """Soft delete the record by setting is_deleted to True."""
        with transaction.atomic():
            self.is_deleted = True
            self.save(update_fields=["is_deleted"])
            update_change_reason(self, "Soft deleted")

    def restore(self):
        """Restore a soft-deleted record by setting is_deleted to False."""
        with transaction.atomic():
            self.is_deleted = False
            self.save(update_fields=["is_deleted"])
            update_change_reason(self, "Restored")

    def hard_delete(self, using=None, keep_parents=False):
        """Permanently delete the record. History entry is not created."""
        super().delete(using=using, keep_parents=keep_parents)
