from django.db.models import Exists, OuterRef

from employee.models import DailySalary, Piecework


def get_deletable_and_blocked_daily_salaries(ids, department):
    """Splits DailySalary queryset into blocked and deletable sets based on related Piecework existence for bulk operations."""
    piecework_exists = Piecework.objects.filter(
        employee_id=OuterRef("employee_id"),
        work_date=OuterRef("salary_date"),
    )

    base_qs = (
        DailySalary.objects.filter(pk__in=ids, department=department)
        .select_related("employee")
        .annotate(has_piecework=Exists(piecework_exists))
    )

    blocked_qs = base_qs.filter(has_piecework=True)
    deletable_qs = base_qs.filter(has_piecework=False)

    return blocked_qs, deletable_qs
