from django.db.models import Prefetch

from employee.models import DailyWork, Piecework


def get_bulk_daily_work_qs(ids, department):
    '''
    This code provides an optimized queryset for bulk operations on DailyWork records, prefetching related Piecework and Employee data to avoid N+1 query issues and improve performance during batch processing.
    '''
    return (
        DailyWork.objects
        .filter(pk__in=ids, department=department)
        .select_related("work")
        .prefetch_related(
            Prefetch(
                "pieceworks",
                queryset=Piecework.objects.select_related("employee"),
                to_attr="prefetched_pieceworks"
            )
        )
    )
