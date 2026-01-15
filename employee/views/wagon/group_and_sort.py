from employee.constants.constants import GROUP_MONTH
from employee.utils.sorting import apply_ordering
from employee.views.wagon.wagon_grouping import get_grouped_wagons


def group_and_sort_wagons(
    qs,
    *,
    group: str | None,
    month: int | None = None,
    year: int | None = None,
    order_by: str | None = None,
    direction: str | None = None,
):
    """
    Groups the filtered DailyWork queryset (detail vs wagon/month) and then applies ordering.
    Used by list views/exports so grouping + sorting rules stay consistent and year/month sorting
    works only after the queryset is annotated with those fields.
    """
    grouped = get_grouped_wagons(qs, group=group, month=month, year=year)

    if group == GROUP_MONTH:
        return apply_ordering(
            grouped,
            order_by,
            direction,
            allowed_fields=["wagon_number", "type_wagon", "month", "year"],
            default=["-year", "-month", "wagon_number", "type_wagon"],
        )

    return apply_ordering(
        grouped,
        order_by,
        direction,
        allowed_fields=["work_date", "work__work_name", "type_work", "wagon_number", "type_wagon"],
        default="-work_date",
    )
