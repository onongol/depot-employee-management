from employee.utils.select_department import get_selected_department
from employee.utils.wagon_department import is_wagon_department


class WagonContextMixin:
    """Add is_wagon_department flag based on department."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = getattr(self, "object", None)
        dept = (obj.department if obj is not None else None) or get_selected_department(
            self.request
        )
        context["is_wagon_department"] = is_wagon_department(dept)
        return context
