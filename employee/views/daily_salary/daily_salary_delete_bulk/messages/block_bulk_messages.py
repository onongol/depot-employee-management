from django.contrib import messages
from django.utils.translation import gettext_lazy as _


def block_bulk_messages(request, blocked_count, blocked_items, blocked_tail):
    """Shows a success message after bulk deletion, including a preview of deleted items for clear user feedback."""
    if blocked_count:
        messages.info(
            request,
            _(
                "Cannot delete %(count)s record(s) because they are associated with Daily Work / Piecework: %(items)s%(tail)s"
            )
            % {
                "count": blocked_count,
                "items": ", ".join(blocked_items),
                "tail": blocked_tail,
            },
        )
