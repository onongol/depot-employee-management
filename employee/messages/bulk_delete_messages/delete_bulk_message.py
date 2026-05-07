from django.contrib import messages
from django.utils.translation import gettext as _


def delete_bulk_message(
    request,
    deleted_count,
    deletable_items=None,
    deletable_tail="",
):
    """Displays a success message after bulk deletion, showing a preview of deleted items and a summary tail for user feedback."""
    deletable_items = deletable_items or []

    if deleted_count:
        messages.success(
            request,
            _("Deleted %(count)s record(s): %(items)s%(tail)s")
            % {
                "count": deleted_count,
                "items": ", ".join(deletable_items),
                "tail": deletable_tail,
            },
        )
