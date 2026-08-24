from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import (
    ChoicesDropdownFilter,
    FieldTextFilter,
    MultipleChoicesDropdownFilter,
)

from employee.admins.common import ReadOnlyExportAdminMixin
from employee.models import DailyWork


@admin.register(DailyWork)
class DailyWorkAdmin(
    ReadOnlyExportAdminMixin,
    ModelAdmin,
    SimpleHistoryAdmin,
):
    list_display = (
        "work_name",
        "department",
        "job_title",
        "type_work",
        "wagon_number",
        "type_wagon",
        "amount",
        "amount_time",
        "amount_price",
        "amount_material",
        "work_date",
        "record_date",
    )
    search_fields = ("work_name",)
    search_help_text = "Search by work name"
    list_filter_submit = True
    list_filter = [
        "department",
        ("job_title", ChoicesDropdownFilter),
        ("wagon_number", FieldTextFilter),
        ("type_work", MultipleChoicesDropdownFilter),
        ("type_wagon", MultipleChoicesDropdownFilter),
    ]
    date_hierarchy = "work_date"
    ordering = ("-work_date", "-record_date")
    list_display_links = ("work_name",)
