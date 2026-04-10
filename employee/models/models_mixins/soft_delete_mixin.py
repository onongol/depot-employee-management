from simple_history.utils import update_change_reason


class SoftDeleteMixin:
    def delete(self, using=None, keep_parents=False):
        """Soft delete the record by setting is_deleted to True."""
        self.is_deleted = True
        self.save(update_fields=["is_deleted"])
        update_change_reason(self, "Soft deleted")

    def restore(self):
        """Restore a soft-deleted record by setting is_deleted to False."""
        self.is_deleted = False
        self.save(update_fields=["is_deleted"])
        update_change_reason(self, "Restored")

    def hard_delete(self, using=None, keep_parents=False):
        """Permanently delete the record from the database."""
        super().delete(using=using, keep_parents=keep_parents)
