from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import (
    ChoicesDropdownFilter,
    MultipleChoicesDropdownFilter,
)

from employee.admins.common import ImportExportMixin
from employee.models import Work


@admin.register(Work)
class WorkAdmin(
    ModelAdmin, SimpleHistoryAdmin, ImportExportModelAdmin, ImportExportMixin
):
    list_display = (
        "work_id",
        "work_name",
        "department",
        "job_title",
        "type_wagon",
        "type_material",
        "usage_material",
        "standard_time",
        "price",
    )
    search_fields = ("work_name",)
    search_help_text = "Search by work name"
    list_filter_submit = True
    list_filter = [
        "department",
        ("job_title", ChoicesDropdownFilter),
        ("type_wagon", MultipleChoicesDropdownFilter),
    ]
    readonly_fields = ("work_id",)
    ordering = ("-work_id",)
    list_display_links = ("work_name",)
