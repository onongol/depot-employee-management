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
