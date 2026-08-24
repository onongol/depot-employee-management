from import_export.admin import (
    ExportActionModelAdmin,
    ExportMixin,
)
from unfold.contrib.import_export.forms import ExportForm, ImportForm


class ImportExportMixin:
    import_form_class = ImportForm
    export_form_class = ExportForm


class ReadOnlyAdminMixin:
    def has_add_permission(self, _request):
        return False

    def has_change_permission(self, _request, _obj=None):
        return False

    def has_delete_permission(self, _request, _obj=None):
        return False


class ReadOnlyExportAdminMixin(
    ReadOnlyAdminMixin,
    ExportActionModelAdmin,
    ExportMixin,
):
    export_form_class = ExportForm


class SoftDeleteAdminMixin:
    """
    Mixin to handle soft deletion in the admin interface.
    It overrides the default queryset and delete behavior.
    """

    def get_queryset(self, request):
        """Override to use the custom manager that includes soft-deleted records."""
        queryset = super().get_queryset(request)
        manager = getattr(self.model, "all_objects", None)
        return manager.all() if manager is not None else queryset

    def delete_queryset(self, _request, queryset):
        """Override to perform soft delete instead of hard delete."""
        for obj in queryset:
            obj.delete()

    def delete_model(self, _request, obj):
        """Override to perform soft delete instead of hard delete."""
        obj.delete()
