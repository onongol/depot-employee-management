from employee.messages.delete_warning import send_delete_warning


class DeleteWarningMixin:
    """Mixin to add delete warning and prevent deletion if related objects exist."""
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()        
        object_name = self.get_object_name()
        response = super().post(request, *args, **kwargs)
        send_delete_warning(request, object_name)
        return response
