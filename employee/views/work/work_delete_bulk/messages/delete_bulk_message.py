from django.contrib import messages
from django.utils.translation import gettext_lazy as _


def delete_bulk_message(request, deleted_count, deletable_items, deletable_tail):
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
