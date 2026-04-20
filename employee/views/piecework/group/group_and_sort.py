from employee.utils.filters import filter_month_year
from employee.utils.sorting import apply_ordering
from employee.views.piecework.group.group_by_month import group_pieceworks_by_month
from employee.views.piecework.group.group_by_year import group_pieceworks_by_year


def group_and_sort_pieceworks(qs, context):
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
            qs = filter_month_year(qs, month=month, year=year, date_field="work_date")

        qs = group_pieceworks_by_month(qs, show_wagon=show_wagon)

        allowed_fields = [
            "employee_code",
            "employee_name",
            "job_title",
            "work_name",
            "type_work",
            "year",
            "month",
        ]
        if show_wagon:
            allowed_fields += ["type_wagon", "wagon_number"]

        qs = apply_ordering(
            qs,
            order_by,
            direction,
            allowed_fields=allowed_fields,
            default=["-year", "-month", "employee_code"],
        )

    elif year_group:
        if selected_year:
            qs = filter_month_year(qs, year=selected_year, date_field="work_date")

        qs = group_pieceworks_by_year(qs, show_wagon=show_wagon)

        allowed_fields = [
            "employee_code",
            "employee_name",
            "job_title",
            "work_name",
            "type_work",
            "year",
        ]

        if show_wagon:
            allowed_fields += ["type_wagon", "wagon_number"]

        qs = apply_ordering(
            qs,
            order_by,
            direction,
            allowed_fields=allowed_fields,
            default=["-year", "employee_code"],
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
