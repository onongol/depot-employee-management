from employee.utils.select_department import get_selected_department


class InitialDepartmentMixin:
    """Populate 'department' in form initial from user selection."""

    def get_initial(self):
        initial = super().get_initial()
        initial["department"] = get_selected_department(self.request)
        return initial
