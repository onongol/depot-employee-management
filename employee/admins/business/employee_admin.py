from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import ChoicesDropdownFilter

from employee.admins.common import ImportExportMixin
from employee.models import Employee


@admin.register(Employee)
class EmployeeAdmin(
    ModelAdmin, SimpleHistoryAdmin, ImportExportModelAdmin, ImportExportMixin
):
    list_display = (
        "employee_id",
        "name",
        "department",
        "job_title",
        "rank",
        "money_per_hour",
        "is_active",
    )
    search_fields = (
        "employee_id",
        "name",
    )
    search_help_text = "Search by employee ID or name"
    list_filter_submit = True
    list_filter = ["department", ("job_title", ChoicesDropdownFilter), "is_active"]
    list_editable = ("is_active",)
    ordering = ("-employee_id",)
    list_display_links = (
        "employee_id",
        "name",
    )
