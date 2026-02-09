from django.contrib import messages
from django.utils.translation import gettext_lazy as _


def send_delete_success_message(request, object_name):
    """Send a warning message after deleting an object."""
    messages.success(
        request,
        _(
            "Deleted %(object_name)s"
        )
        % {"object_name": object_name},
    )
