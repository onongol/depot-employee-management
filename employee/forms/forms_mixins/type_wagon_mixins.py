from employee.constants.constants import (ALLOWED_WAGON_DEPARTMENTS, 
                                          EMPTY_SELECT, 
                                          TYPE_WAGON_CHOICES)


class TypeWagonChoicesMixin:
    """Mixin to dynamically set type_wagon choices based on department."""
    def _resolve_department(self, department=None):
        return (
            department
            or (self.data.get('department') if getattr(self, 'is_bound', False) else None)
            or getattr(self.instance, 'department', None)
            or self.initial.get('department')
        )

    def __init__(self, *args, **kwargs):
        department = kwargs.pop('department', None)
        super().__init__(*args, **kwargs)
        dept = self._resolve_department(department)
        if 'type_wagon' in self.fields:
            if dept in set(ALLOWED_WAGON_DEPARTMENTS):
                self.fields['type_wagon'].choices = EMPTY_SELECT + list(TYPE_WAGON_CHOICES)
            else:
                self.fields['type_wagon'].choices = EMPTY_SELECT
            self.fields['type_wagon'].initial = None
