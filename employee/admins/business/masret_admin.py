from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin

from employee.admins.common import ImportExportMixin
from employee.models import Master


@admin.register(Master)
class MasterAdmin(
    ModelAdmin, SimpleHistoryAdmin, ImportExportModelAdmin, ImportExportMixin
):
    list_display = (
        "master_id",
        "name",
        "department",
        "is_active",
    )
    search_fields = (
        "master_id",
        "name",
    )
    search_help_text = "Search by master ID or name"
    list_filter = ["department", "is_active"]
    list_editable = ("is_active",)
    ordering = ("-master_id",)
    list_display_links = (
        "master_id",
        "name",
    )
