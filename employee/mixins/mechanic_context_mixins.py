from employee.constants.constants import MECHANIC
from employee.utils.select_department import get_selected_department


class MechanicContextMixin:
    """Add MECHANIC constant to context."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dept = getattr(
            getattr(self, "object", None), "department", None
        ) or get_selected_department(self.request)
        context["MECHANIC"] = dept == MECHANIC
        return context
