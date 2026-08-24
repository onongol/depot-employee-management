from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.db.models import Exists, OuterRef
from django.utils.translation import gettext_lazy as _

from employee.admins.log_entry.type_label import get_content_type_label


class LogEntryModelFilter(admin.SimpleListFilter):
    """Custom admin filter for LogEntry content types (models)."""

    title = _("Model")
    parameter_name = "content_type"

    def lookups(self, _request, model_admin):
        has_logentry = model_admin.model.objects.filter(
            content_type_id=OuterRef("pk"),
        )

        content_types = (
            ContentType.objects.annotate(has_logentry=Exists(has_logentry))
            .filter(has_logentry=True)
            .order_by("app_label", "model")
        )

        return [
            (str(content_type.pk), get_content_type_label(content_type))
            for content_type in content_types
        ]

    def queryset(self, _request, queryset):
        value = self.value()
        if value is None:
            return queryset
        try:
            return queryset.filter(content_type_id=int(value))
        except (TypeError, ValueError):
            return queryset.none()
