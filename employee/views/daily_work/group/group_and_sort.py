from employee.utils.sorting import apply_ordering
from employee.views.daily_work.group.group_by_month import group_daily_works_by_month
from employee.views.daily_work.group.group_by_year import group_daily_works_by_year


def group_and_sort_daily_works(qs, context):
    """
    Applies grouping (monthly/yearly) and ordering to DailyWork querysets.
    Optionally filters by month/year, aggregates totals via group_by_month/year,
    and enforces safe ordering fields (including wagon columns only when relevant).
    Used by both list views and exports to keep behavior consistent.
    """
    month_group = context.month_group
    year_group = context.year_group
    month = context.month
    year = context.year
    selected_year = context.selected_year
    show_wagon = context.show_wagon
    order_by = context.order_by
    direction = context.direction

    if month_group:
        if month and year:
            qs = qs.filter(work_month=month, work_year=year)

        qs = group_daily_works_by_month(qs, show_wagon=show_wagon)

        allowed_fields = ["work_name", "job_title", "type_work", "year", "month"]
        if show_wagon:
            allowed_fields += ["type_wagon", "wagon_number"]

        qs = apply_ordering(
            qs,
            order_by,
            direction,
            allowed_fields=allowed_fields,
            default=["-year", "-month", "work_name"],
        )
    elif year_group:
        if selected_year:
            qs = qs.filter(work_year=selected_year)

        qs = group_daily_works_by_year(qs, show_wagon=show_wagon)

        allowed_fields = ["work_name", "job_title", "type_work", "year"]
        if show_wagon:
            allowed_fields += ["type_wagon", "wagon_number"]

        qs = apply_ordering(
            qs,
            order_by,
            direction,
            allowed_fields=allowed_fields,
            default=["-year", "work_name"],
        )
    else:
        qs = apply_ordering(
            qs,
            order_by,
            direction,
            allowed_fields=["work_date", "record_date"],
            default=["-work_date", "-record_date"],
        )

    return qs
