from employee.constants.constants import GROUP_MONTH, GROUP_YEAR
from employee.utils.filters import filter_month_year
from employee.utils.sorting import apply_ordering
from employee.views.daily_work.group_by_month import group_daily_works_by_month
from employee.views.daily_work.group_by_year import group_daily_works_by_year    


def group_and_sort(
    daily_works,
    *,
    group: str | None,
    month: int | None = None,
    year: int | None = None,
    selected_year: str = "",
    show_wagon: bool = False,
    order_by: str | None = None,
    direction: str | None = None,
):
    
    if group == GROUP_MONTH:
        if month and year:
            daily_works = filter_month_year(daily_works, month=month, year=year, date_field="work_date")

        daily_works = group_daily_works_by_month(daily_works, show_wagon=show_wagon)

        daily_works = apply_ordering(
            daily_works,
            order_by,
            direction,
            allowed_fields=['work_name', 'job_title', 'type_work', 'type_wagon', 'wagon_number', 'year', 'month'],
            default=['-year', '-month', 'work_name']
        )
    elif group == GROUP_YEAR:
        if selected_year:
            daily_works = filter_month_year(daily_works, year=selected_year, date_field="work_date")

        daily_works = group_daily_works_by_year(daily_works, show_wagon=show_wagon)

        daily_works = apply_ordering(
            daily_works,
            order_by,
            direction,
            allowed_fields=['work_name', 'job_title', 'type_work', 'type_wagon', 'wagon_number', 'year'],
            default=['-year', 'work_name']
        )
    else:
        daily_works = apply_ordering(
            daily_works,
            order_by,
            direction,
            allowed_fields=['work_date', 'record_date'],
            default=['-work_date', '-record_date']
        )

    return daily_works
