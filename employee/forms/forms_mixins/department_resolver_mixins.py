class DepartmentResolverMixin:
    """Resolve department from bound data, initial data, or model instance."""

    def get_department(self):
        if getattr(self, "is_bound", False):
            return self.data.get("department") or self.initial.get("department")
        return self.initial.get("department") or getattr(
            getattr(self, "instance", None), "department", None
        )
