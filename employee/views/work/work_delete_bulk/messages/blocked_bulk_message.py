from django.contrib import messages
from django.utils.translation import gettext_lazy as _


def blocked_bulk_message(request, blocked_count, blocked_items, blocked_tail):
    template = _(
        "Cannot delete %(count)s record(s): %(items)s%(tail)s. Linked to existing entries."
    )

    if blocked_count:
        messages.warning(
            request,
            template
            % {
                "count": blocked_count,
                "items": ", ".join(blocked_items),
                "tail": blocked_tail,
            },
        )
