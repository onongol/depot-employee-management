from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


@admin.display(description="Action")
def action_label(self, obj):
    if obj.is_addition():
        label = _("Added")
        styles = "background:#dcfce7;color:#166534;"
    elif obj.is_deletion():
        label = _("Deleted")
        styles = "background:#fee2e2;color:#991b1b;"
    elif obj.is_change():
        label = _("Changed")
        styles = "background:#dbeafe;color:#1d4ed8;"
    else:
        label = obj.get_action_flag_display()
        styles = "background:#e5e7eb;color:#374151;"

    return format_html(
        '<span style="display:inline-block;padding:0.2rem 0.55rem;border-radius:9999px;font-weight:600;{}">{}</span>',
        styles,
        label,
    )
