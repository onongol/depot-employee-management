from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import ChoicesDropdownFilter

from employee.admins.common import ReadOnlyExportAdminMixin
from employee.models import DailySalary


@admin.register(DailySalary)
class DailySalaryAdmin(
    ReadOnlyExportAdminMixin,
    ModelAdmin,
    SimpleHistoryAdmin,
):
    list_display = (
        "employee_code",
        "employee_name",
        "department",
        "job_title",
        "hours_per_day",
        "salary_day",
        "salary_date",
        "record_date",
    )
    search_fields = (
        "employee_code__exact",
        "employee_name",
    )
    search_help_text = "Search by employee code or name"
    list_filter_submit = True
    list_filter = [
        "department",
        ("job_title", ChoicesDropdownFilter),
    ]
    date_hierarchy = "salary_date"
    ordering = ("-salary_date", "-record_date")
    list_display_links = (
        "employee_code",
        "employee_name",
    )
