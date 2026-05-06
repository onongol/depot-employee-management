from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import (
    ChoicesDropdownFilter,
    FieldTextFilter,
    MultipleChoicesDropdownFilter,
)

from employee.admins.common import ReadOnlyExportAdminMixin
from employee.models import Piecework


@admin.register(Piecework)
class PieceworkAdmin(
    ReadOnlyExportAdminMixin,
    ModelAdmin,
    SimpleHistoryAdmin,
):
    list_display = (
        "employee_code",
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
        "employee_code__exact",
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
    date_hierarchy = "work_date"
    ordering = ("-work_date", "-record_date")
    list_display_links = ("employee_code", "employee_name", "work_name")
