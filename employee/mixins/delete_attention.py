from django.contrib import messages


def send_delete_warning(request, object_name):
    """Send a warning message after deleting an object."""
    messages.warning(
        request,
        f'You have deleted {object_name}. Also, all related records have been deleted.'
    )
