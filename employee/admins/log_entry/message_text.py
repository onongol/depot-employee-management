from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.display(description="Message")
def message_text(self, obj):
    message = obj.get_change_message()
    if message:
        return message
    if obj.is_change():
        return _("Changed")
    return ""
