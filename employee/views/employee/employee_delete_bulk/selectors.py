from django.db.models import Exists, OuterRef

from employee.models.employee_models import Employee
from employee.models.piecework_models import Piecework


def get_deletable_and_blocked_employees(ids, department):
    """Splits Employee queryset into blocked and deletable sets based on related DailyWork or Piecework existence for bulk operations."""
    piecework_exists = Piecework.objects.filter(employee=OuterRef("pk"))

    base_qs = Employee.objects.filter(pk__in=ids, department=department).annotate(
        has_piecework=Exists(piecework_exists),
    )

    blocked_qs = base_qs.filter(has_piecework=True)
    blocked_qs = blocked_qs.distinct()
    deletable_qs = base_qs.filter(has_piecework=False)

    return blocked_qs, deletable_qs
