from employee.constants.constants import get_type_work_choices
from employee.forms.forms_mixins.department_resolver_mixins import (
    DepartmentResolverMixin,
)


class TypeWorkChoicesMixin(DepartmentResolverMixin):
    """Set type_work choices based on the resolved department."""

    def __init__(self, *args, department=None, **kwargs):
        super().__init__(*args, **kwargs)

        if "type_work" in self.fields:
            self.fields["type_work"].choices = get_type_work_choices(
                department or self.get_department()
            )
