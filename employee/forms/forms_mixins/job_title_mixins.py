from employee.constants.constants import get_job_title_choices
from employee.forms.forms_mixins.department_resolver_mixins import (
    DepartmentResolverMixin,
)


class JobTitleChoicesMixin(DepartmentResolverMixin):
    """Set job_title choices based on the resolved department."""

    def __init__(self, *args, department=None, **kwargs):
        super().__init__(*args, **kwargs)

        if "job_title" in self.fields:
            self.fields["job_title"].choices = get_job_title_choices(
                department or self.get_department()
            )
