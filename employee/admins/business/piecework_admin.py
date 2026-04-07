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
from employee.models import Piecework


@admin.register(Piecework)
class PieceworkAdmin(
    ReadOnlyAdminMixin, ModelAdmin, ExportActionModelAdmin, ExportMixin, ExportForm
):
    list_display = (
        "record_id",
        "employee_id",
        "employee_name",
        "department",
        "job_title",
        "work_name",
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
    search_fields = (
        "employee__employee_id",
        "employee_name",
    )
    search_help_text = "Search by employee ID or name"
    list_filter_submit = True
    list_filter = [
        "department",
        ("job_title", ChoicesDropdownFilter),
        ("work_name", FieldTextFilter),
        "type_work",
        ("wagon_number", FieldTextFilter),
        ("type_wagon", MultipleChoicesDropdownFilter),
    ]
    list_select_related = ("employee", "work", "daily_work")
    date_hierarchy = "work_date"
    ordering = ("-work_date", "-record_date")
    list_display_links = None
