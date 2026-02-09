from employee.utils.select_department import get_selected_department


class GenericContextMixin:
    """Generic mixin to add object name, type, department, and cancel URL to context."""

    model = None
    object_type = None
    object_name_func = None
    success_url = None
    cancel_url = None

    def get_object_name(self, obj=None) -> str:
        """
        Single source of truth for displaying object name across:
        context, modals, messages, delete/update/create flows.
        """
        if obj is None:
            obj = getattr(self, "object", None)
        if not obj:
            return ""
        return str(obj)

    def get_context_data(self, **kwargs):
        """Add object name, type, department, and cancel URL to context."""
        context = super().get_context_data(**kwargs)
        obj = getattr(self, "object", None)

        # Get selected department from request GET parameters or session
        department = get_selected_department(self.request)

        context["selected_department"] = department

        # Get object name using the provided function or str()
        context["object_name"] = self.get_object_name(obj)
        context["object_type"] = self.object_type
        context["cancel_url"] = self.cancel_url

        return context
