from django.contrib import messages
from django.utils.translation import gettext_lazy as _


def send_delete_warning(request, object_name):
    """Send a warning message after deleting an object."""
    messages.warning(
        request,
        _(
            "You have deleted %(object_name)s. Also, all related records have been deleted."
        )
        % {"object_name": object_name},
    )
