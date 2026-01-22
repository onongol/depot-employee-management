from employee.constants.constants import get_job_title_choices


class JobTitleChoicesMixin:
    """Mixin to dynamically set job title choices based on department."""

    def _resolve_department(self, department=None):
        return (
            department
            or (
                self.data.get("department")
                if getattr(self, "is_bound", False)
                else None
            )
            or getattr(self.instance, "department", None)
            or self.initial.get("department")
        )

    def __init__(self, *args, **kwargs):
        department = kwargs.pop("department", None)
        super().__init__(*args, **kwargs)
        dept = self._resolve_department(department)
        if "job_title" in self.fields:
            self.fields["job_title"].choices = get_job_title_choices(dept)
