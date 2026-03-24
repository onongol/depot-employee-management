from django.db.models import Exists, OuterRef

from employee.models.daily_work_models import DailyWork
from employee.models.employee_models import Employee
from employee.models.piecework_models import Piecework


def get_deletable_and_blocked_employees(ids, department):
    """Splits Employee queryset into blocked and deletable sets based on related DailyWork or Piecework existence for bulk operations."""
    dailywork_exists = DailyWork.objects.filter(work=OuterRef("pk"))
    piecework_exists = Piecework.objects.filter(work=OuterRef("pk"))

    base_qs = Employee.objects.filter(pk__in=ids, department=department).annotate(
        has_dailywork=Exists(dailywork_exists),
        has_piecework=Exists(piecework_exists),
    )

    blocked_qs = base_qs.filter(has_dailywork=True, has_piecework=True)
    blocked_qs = blocked_qs.distinct()
    deletable_qs = base_qs.filter(has_dailywork=False, has_piecework=False)

    return blocked_qs, deletable_qs
