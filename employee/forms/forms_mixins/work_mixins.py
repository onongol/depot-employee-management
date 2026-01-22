from django.utils.translation import gettext_lazy as _

from employee.models import Work


class WorkNameUniqueMixin:
    """Mixin to ensure work_name is unique within the department."""

    def clean_work_name(self):
        work_name = self.cleaned_data.get("work_name")
        department = (
            self.cleaned_data.get("department")
            or self.initial.get("department")
            or (
                self.data.get("department")
                if getattr(self, "is_bound", False)
                else None
            )
            or getattr(self.instance, "department", None)
        )
        if work_name and department:
            qs = Work.objects.filter(work_name=work_name, department=department)
            if getattr(self.instance, "pk", None):
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error(
                    "work_name",
                    _("The Work Name must be unique within the department."),
                )
        return work_name
