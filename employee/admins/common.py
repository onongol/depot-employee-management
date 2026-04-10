from import_export.admin import (
    ExportActionModelAdmin,
    ExportMixin,
    ImportExportModelAdmin,
)
from unfold.contrib.import_export.forms import ExportForm, ImportForm


class ImportExportMixin:
    import_form_class = ImportForm
    export_form_class = ExportForm


class ReadOnlyAdminMixin:
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ReadOnlyExportAdminMixin(
    ReadOnlyAdminMixin,
    ExportActionModelAdmin,
    ExportMixin,
    ExportForm,
):
    pass


class ReadOnlyImportExportAdminMixin(
    ReadOnlyAdminMixin,
    ImportExportModelAdmin,
    ImportExportMixin,
):
    pass


class SoftDeleteAdminMixin:
    """Mixin to handle soft deletion in the admin interface. It overrides the default queryset and delete behavior."""

    def get_queryset(self, request):
        """Override to use the custom manager that includes soft-deleted records."""
        return self.model.all_objects.all()

    def delete_queryset(self, request, queryset):
        """Override to perform soft delete instead of hard delete."""
        for obj in queryset:
            obj.delete()

    def delete_model(self, request, obj):
        """Override to perform soft delete instead of hard delete."""
        obj.delete()
