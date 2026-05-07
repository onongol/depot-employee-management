from employee.constants.constants import MECHANIC
from employee.utils.select_department import get_selected_department


class MechanicContextMixin:
    """Add is_mechanic flag to context."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = getattr(self, "object", None)
        dept = (obj.department if obj is not None else None) or get_selected_department(
            self.request
        )
        context["is_mechanic"] = dept == MECHANIC
        return context
