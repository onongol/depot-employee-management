from django.contrib import admin
from django.contrib.admin.models import LogEntry
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import FieldTextFilter, RangeDateFilter

from employee.admins.common import ReadOnlyAdminMixin
from employee.admins.log_entry.action_label import action_label
from employee.admins.log_entry.display_col_head import make_logentry_display
from employee.admins.log_entry.log_actions_filters import LogEntryActionFilter
from employee.admins.log_entry.log_model_filters import LogEntryModelFilter
from employee.admins.log_entry.message_text import message_text
from employee.admins.log_entry.model_name import model_name


@admin.register(LogEntry)
class LogEntryAdmin(ReadOnlyAdminMixin, ModelAdmin):
    list_display = (
        "log_object",
        "logged_at",
        "action_label",
        "performed_by",
        "model_name",
        "message_text",
    )
    search_fields = ("object_repr",)
    search_help_text = "Search by object representation"
    list_filter_submit = True
    list_filter = (
        ("action_time", RangeDateFilter),
        LogEntryActionFilter,
        ("user__username", FieldTextFilter),
        LogEntryModelFilter,
    )
    list_select_related = ("user", "content_type")
    ordering = ("-action_time",)
    list_display_links = None

    log_object = make_logentry_display("object_repr", "Object")
    logged_at = make_logentry_display("action_time", "Date/Time")
    performed_by = make_logentry_display("user", "User")

    model_name = model_name
    action_label = action_label
    message_text = message_text
