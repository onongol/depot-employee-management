from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from employee.admins.log_entry.type_label import get_content_type_label


class LogEntryModelFilter(admin.SimpleListFilter):
    """Custom admin filter for LogEntry content types (models)."""
    title = _("Model")
    parameter_name = "content_type"

    def lookups(self, request, model_admin):
        content_type_ids = (
            model_admin.model.objects.exclude(content_type__isnull=True)
            .values_list("content_type_id", flat=True)
            .distinct()
        )
        content_types = ContentType.objects.filter(id__in=content_type_ids).order_by(
            "app_label", "model"
        )
        return [
            (str(content_type.pk), get_content_type_label(content_type))
            for content_type in content_types
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(content_type_id=self.value())
        return queryset
