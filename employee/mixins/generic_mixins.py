from employee.utils.select_department import get_selected_department


class GenericContextMixin:
    """Generic mixin to add object name, type, department, and cancel URL to context."""

    model = None
    object_type = None

    def get_object_name(self, obj=None) -> str:
        """
        Single source of truth for displaying object name across:
        context, modals, messages, delete/update/create flows.
        """
        obj = obj if obj is not None else getattr(self, "object", None)
        return str(obj) if obj is not None else ""

    def get_context_data(self, **kwargs):
        """Add object name, type, department, and cancel URL to context."""
        context = super().get_context_data(**kwargs)
        obj = getattr(self, "object", None)
        department = get_selected_department(self.request)

        context["selected_department"] = department
        context["object_name"] = self.get_object_name(obj)
        context["object_type"] = self.object_type
        context["cancel_url"] = self.cancel_url

        return context
