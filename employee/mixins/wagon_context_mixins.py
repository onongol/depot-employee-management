from employee.utils.select_department import get_selected_department
from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS


class WagonContextMixin:
    """Add SHOW_TYPE_WAGON flag based on department."""
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        dept = getattr(getattr(self, 'object', None), 'department', None) or get_selected_department(self.request)
        ctx['SHOW_TYPE_WAGON'] = dept in ALLOWED_WAGON_DEPARTMENTS
        return ctx
