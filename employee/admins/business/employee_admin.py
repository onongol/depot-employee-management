from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import ChoicesDropdownFilter

from employee.admins.common import ImportExportMixin, SoftDeleteAdminMixin
from employee.models import Employee


@admin.register(Employee)
class EmployeeAdmin(
    SoftDeleteAdminMixin,
    ModelAdmin,
    SimpleHistoryAdmin,
    ImportExportModelAdmin,
    ImportExportMixin,
):
    list_display = (
        "employee_id",
        "employee_name",
        "department",
        "job_title",
        "rank",
        "money_per_hour",
        "is_active",
        "is_deleted",
    )
    search_fields = (
        "employee_id__exact",
        "employee_name",
    )
    search_help_text = "Search by employee ID or name"
    list_filter_submit = True
    list_filter = [
        "department",
        ("job_title", ChoicesDropdownFilter),
        "is_active",
        "is_deleted",
    ]
    list_editable = ("is_active",)
    ordering = ("-employee_id",)
    list_display_links = (
        "employee_id",
        "employee_name",
    )
