from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin

from employee.admins.common import ImportExportMixin, SoftDeleteAdminMixin
from employee.models import Payroll


@admin.register(Payroll)
class PayrollAdmin(
    SoftDeleteAdminMixin,
    ModelAdmin,
    SimpleHistoryAdmin,
    ImportExportModelAdmin,
    ImportExportMixin,
):
    list_display = (
        "payroll_id",
        "name",
        "is_active",
        "is_deleted",
    )
    search_fields = (
        "payroll_id",
        "name",
    )
    search_help_text = "Search by payroll ID or name"
    list_filter = ["is_active", "is_deleted"]
    list_editable = ("is_active",)
    ordering = ("-payroll_id",)
    list_display_links = (
        "payroll_id",
        "name",
    )
