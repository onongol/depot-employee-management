from employee.constants.constants import get_type_work_choices


class TypeWorkChoiceMixin:
    """Mixin to set type work choices based on department."""
    def __init__(self, *args, **kwargs):
        department = kwargs.pop('department', None)
        super().__init__(*args, **kwargs)
        if 'type_work' in self.fields:
            self.fields['type_work'].choices = get_type_work_choices(department)
