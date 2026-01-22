from employee.constants.constants import get_job_title_choices


class JobTitleChoicesMixin:
    """Mixin: set job_title choices based on department."""

    def __init__(self, *args, department=None, **kwargs):
        super().__init__(*args, **kwargs)
        dept = department
        if dept is None:
            dept = (
                (
                    self.data.get("department")
                    if getattr(self, "is_bound", False)
                    else None
                )
                or self.initial.get("department")
                or getattr(getattr(self, "instance", None), "department", None)
            )
        if "job_title" in self.fields:
            self.fields["job_title"].choices = get_job_title_choices(dept)
