from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from employee.admins.log_entry.type_label import get_content_type_label


@admin.display(description=_("Model"))
def model_name(_self, obj):
    """Admin display callback to show the content type (model) label for a LogEntry."""
    return get_content_type_label(obj.content_type)
