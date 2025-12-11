from django.contrib import messages
from django.shortcuts import redirect

from employee.mixins.delete_messages import send_delete_warning


class DeleteWarningMixin:
    """Mixin to add delete warning and prevent deletion if related objects exist."""
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()        
        object_name = self.get_object_name()
        response = super().post(request, *args, **kwargs)
        send_delete_warning(request, object_name)
        return response

   
class DeleteProtectionMixin:
    """Mixin to check for delete attentions before allowing deletion."""
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Check for related objects
        related_objects = self.get_related_objects()
        if related_objects and related_objects.exists():
            messages.info(request, self.get_block_message())
            return redirect(self.get_redirect_url())

        object_name = self.get_object_name()
        response = super().post(request, *args, **kwargs)
        send_delete_warning(request, object_name)
        return response
