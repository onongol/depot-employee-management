from django.contrib import messages
from django.shortcuts import redirect

from employee.messages.delete_success_message import send_delete_success_message


class DeleteProtectionMixin:
    """Mixin to check for delete attentions before allowing deletion."""

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Check for related objects
        related_objects = self.get_related_objects()
        if related_objects and related_objects.exists():
            messages.warning(request, self.get_block_message())
            return redirect(self.get_redirect_url())

        object_name = self.get_object_name()
        response = super().post(request, *args, **kwargs)
        send_delete_success_message(request, object_name)
        return response
