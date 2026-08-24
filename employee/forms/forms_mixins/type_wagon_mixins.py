from employee.constants.constants import (
    ALLOWED_WAGON_DEPARTMENTS,
    EMPTY_SELECT,
    TYPE_WAGON_CHOICES,
)
from employee.forms.forms_mixins.department_resolver_mixins import (
    DepartmentResolverMixin,
)

ALLOWED_WAGON_DEPARTMENTS_SET = frozenset(ALLOWED_WAGON_DEPARTMENTS)
TYPE_WAGON_WITH_EMPTY = EMPTY_SELECT + list(TYPE_WAGON_CHOICES)


class TypeWagonChoicesMixin(DepartmentResolverMixin):
    """Mixin to dynamically set type_wagon choices based on department."""

    def __init__(self, *args, department=None, **kwargs):
        super().__init__(*args, **kwargs)

        dept = department or self.get_department()
        if "type_wagon" in self.fields:
            if dept in ALLOWED_WAGON_DEPARTMENTS_SET:
                self.fields["type_wagon"].choices = TYPE_WAGON_WITH_EMPTY
            else:
                self.fields["type_wagon"].choices = EMPTY_SELECT
            self.fields["type_wagon"].initial = None
