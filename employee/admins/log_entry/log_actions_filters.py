from django.contrib import admin
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.utils.translation import gettext_lazy as _


class LogEntryActionFilter(admin.SimpleListFilter):
    """Custom admin filter for LogEntry action types (Addition, Change, Deletion)."""

    title = _("Action")
    parameter_name = "action_flag"

    def lookups(self, _request, _model_admin):
        return (
            (str(ADDITION), _("Added")),
            (str(CHANGE), _("Changed")),
            (str(DELETION), _("Deleted")),
        )

    def queryset(self, _request, queryset):
        value = self.value()
        if value is None:
            return queryset
        try:
            return queryset.filter(action_flag=int(value))
        except (TypeError, ValueError):
            return queryset.none()
