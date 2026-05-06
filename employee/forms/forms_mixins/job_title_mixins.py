from employee.constants.constants import get_job_title_choices


class JobTitleChoicesMixin:
    """Set job_title choices based on the resolved department."""

    def __init__(self, *args, department=None, **kwargs):
        super().__init__(*args, **kwargs)

        if "job_title" in self.fields:
            self.fields["job_title"].choices = get_job_title_choices(
                department or self._get_department()
            )

    def _get_department(self):
        if getattr(self, "is_bound", False):
            return self.data.get("department") or self.initial.get("department")
        return self.initial.get("department") or getattr(
            getattr(self, "instance", None), "department", None
        )
