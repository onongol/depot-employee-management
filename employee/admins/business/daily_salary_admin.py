from django.contrib import admin
from import_export.admin import ExportActionModelAdmin, ExportMixin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import ChoicesDropdownFilter
from unfold.contrib.import_export.forms import ExportForm

from employee.admins.common import ReadOnlyAdminMixin
from employee.models import DailySalary


@admin.register(DailySalary)
class DailySalaryAdmin(
    ReadOnlyAdminMixin,
    ModelAdmin,
    SimpleHistoryAdmin,
    ExportActionModelAdmin,
    ExportMixin,
    ExportForm,
):
    list_display = (
        "salary_id",
        "employee_id",
        "employee_name",
        "department",
        "employee__job_title",
        "hours_per_day",
        "salary_day",
        "salary_date",
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
        ("employee__job_title", ChoicesDropdownFilter),
    ]
    list_select_related = ("employee",)
    date_hierarchy = "salary_date"
    ordering = ("-salary_date", "-record_date")
    list_display_links = (
        "employee_id",
        "employee_name",
    )