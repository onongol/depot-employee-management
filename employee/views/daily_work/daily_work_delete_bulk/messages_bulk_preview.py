from typing import List

from django.utils.translation import gettext_lazy as _

from employee.views.daily_work.daily_work_delete_bulk.employees_preview import get_employees_preview


def preview_daily_work_items(base_qs) -> List[str]:
    '''
    This code generates user-friendly preview messages for bulk deletion of DailyWork records, summarizing key details and related employees for each record. It helps inform users about which data will be affected before the operation is performed.
    '''
    parts = []

    for daily_work in base_qs:
        pieceworks = getattr(daily_work, "prefetched_pieceworks", [])
        employees_summary, pieceworks_count = get_employees_preview(pieceworks)

        parts.append(
            _(
                "Deleted Daily Work record: %(work)s on %(date)s with %(pieceworks_count)d related Piecework record(s): %(employees)s."
            ) % {
                "work": daily_work.work.work_name,
                "date": daily_work.work_date,
                "pieceworks_count": pieceworks_count,
                "employees": employees_summary,
            }
        )

    return parts
