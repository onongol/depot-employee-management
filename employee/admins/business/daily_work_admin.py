from django.contrib import admin
from import_export.admin import ExportActionModelAdmin, ExportMixin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import (
    ChoicesDropdownFilter,
    FieldTextFilter,
    MultipleChoicesDropdownFilter,
)
from unfold.contrib.import_export.forms import ExportForm

from employee.admins.common import ReadOnlyAdminMixin
from employee.models import DailyWork


@admin.register(DailyWork)
class DailyWorkAdmin(
    ReadOnlyAdminMixin,
    ModelAdmin,
    SimpleHistoryAdmin,
    ExportActionModelAdmin,
    ExportMixin,
    ExportForm,
):
    list_display = (
        "id",
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
    list_select_related = ("work",)
    date_hierarchy = "work_date"
    ordering = ("-work_date", "-record_date")
    list_display_links = ("work_name",)
