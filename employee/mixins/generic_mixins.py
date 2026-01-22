class GenericContextMixin:
    """Generic mixin to add object name, type, department, and cancel URL to context."""

    model = None
    object_type = None
    object_name_func = None
    success_url = None
    cancel_url = None

    def get_context_data(self, **kwargs):
        """Add object name, type, department, and cancel URL to context."""
        context = super().get_context_data(**kwargs)
        obj = getattr(self, "object", None)

        # Get selected department from request GET parameters or session
        department = self.request.GET.get("department") or self.request.session.get(
            "department"
        )

        context["selected_department"] = department

        # Get object name using the provided function or str()
        if obj:
            if self.object_name_func:
                context["object_name"] = self.object_name_func(obj)
            else:
                context["object_name"] = str(obj)
        else:
            context["object_name"] = ""

        context["object_type"] = self.object_type
        context["cancel_url"] = self.cancel_url
        
        return context
