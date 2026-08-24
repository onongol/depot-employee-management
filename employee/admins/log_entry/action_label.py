from django.contrib import admin
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

ACTION_META = {
    ADDITION: (_("Added"), "background:#dcfce7;color:#166534;"),
    DELETION: (_("Deleted"), "background:#fee2e2;color:#991b1b;"),
    CHANGE: (_("Changed"), "background:#dbeafe;color:#1d4ed8;"),
}
DEFAULT_ACTION_STYLE = "background:#e5e7eb;color:#374151;"

ACTION_BADGE_TEMPLATE = (
    '<span style="display:inline-block;padding:0.2rem 0.55rem;'
    'border-radius:9999px;font-weight:600;{}">{}</span>'
)


@admin.display(description=_("Action"))
def action_label(_self, obj):
    """Admin display callback used by LogEntryAdmin to show the action as a colored badge."""
    label, styles = ACTION_META.get(
        obj.action_flag,
        (obj.get_action_flag_display(), DEFAULT_ACTION_STYLE),
    )

    return format_html(
        ACTION_BADGE_TEMPLATE,
        styles,
        label,
    )
