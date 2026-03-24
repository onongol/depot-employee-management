from django.db.models import Exists, OuterRef

from employee.models.daily_work_models import DailyWork
from employee.models.work_models import Work


def get_deletable_and_blocked_works(ids, department):
    """Splits Work queryset into blocked and deletable sets based on related DailyWork or Piecework existence for bulk operations."""
    dailywork_exists = DailyWork.objects.filter(work=OuterRef("pk"))

    base_qs = Work.objects.filter(pk__in=ids, department=department).annotate(
        has_dailywork=Exists(dailywork_exists),
    )

    blocked_qs = base_qs.filter(has_dailywork=True)
    blocked_qs = blocked_qs.distinct()
    deletable_qs = base_qs.filter(has_dailywork=False)

    return blocked_qs, deletable_qs
