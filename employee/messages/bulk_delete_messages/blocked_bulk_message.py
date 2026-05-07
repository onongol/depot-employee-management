from django.contrib import messages
from django.utils.translation import gettext as _


def blocked_bulk_message(request, blocked_count, blocked_items=None, blocked_tail=""):
    """Send a warning message if there are blocked items that cannot be deleted."""
    if blocked_items is None:
        blocked_items = []

    if blocked_count:
        messages.warning(
            request,
            _(
                "Cannot delete %(count)s record(s): %(items)s%(tail)s. Linked to existing entries."
            )
            % {
                "count": blocked_count,
                "items": ", ".join(blocked_items),
                "tail": blocked_tail,
            },
        )
