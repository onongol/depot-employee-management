from django.db.models import Q, QuerySet

from employee.constants.constants import DEFAULT_WAGON_NUMBER
from employee.models import Piecework


def build_piecework_qs(
    *, employees, month, year, group_by_wagon: bool, wagon_number: str | None
) -> QuerySet:
    """Build the base Piecework queryset with all filters applied before aggregation (date + optional wagon filter)."""
    
    qs = Piecework.objects.filter(employee__in=employees)

    if month:
        qs = qs.filter(work_date__month=month)
    if year:
        qs = qs.filter(work_date__year=year)

    if group_by_wagon and wagon_number:
        if wagon_number == DEFAULT_WAGON_NUMBER:
            qs = qs.filter(
                Q(wagon_number__isnull=True) | Q(wagon_number=DEFAULT_WAGON_NUMBER)
            )
        else:
            qs = qs.filter(wagon_number=wagon_number)

    return qs
