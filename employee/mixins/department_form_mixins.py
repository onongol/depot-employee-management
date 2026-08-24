from employee.utils.select_department import get_selected_department


class FormDepartmentMixin:
    """Inject selected department into form kwargs."""

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["department"] = get_selected_department(self.request)
        return kwargs
