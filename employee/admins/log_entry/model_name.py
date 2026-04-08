from django.contrib import admin

from employee.admins.log_entry.type_label import get_content_type_label


@admin.display(description="Model")
def model_name(self, obj):
    """Admin display callback to show the content type (model) label for a LogEntry."""
    return get_content_type_label(obj.content_type)
