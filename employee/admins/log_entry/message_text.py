from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.display(description=_("Message"))
def message_text(_self, obj):
    """Admin display callback to show the change message or a default label for changes."""
    message = obj.get_change_message()
    if message:
        return message
    if obj.is_change():
        return _("Changed")
    return ""
