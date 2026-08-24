from employee.utils.get_value import get_value


def iter_rows(qs, context):
    """Generate rows for DailyWork export (detailed or grouped)."""
    show_wagon = context.show_wagon
    month_group = context.month_group
    year_group = context.year_group
    grouped = month_group or year_group

    for i, dw in enumerate(qs, start=1):
        work_name = get_value(dw, "work_name", "") or ""
        job_title = get_value(dw, "job_title", "") or ""
        type_work = get_value(dw, "type_work", "") or ""

        if not grouped:
            work_name = (
                work_name or getattr(getattr(dw, "work", None), "work_name", "") or ""
            )

        row = [
            i,
            work_name,
            job_title,
            type_work,
        ]

        if show_wagon:
            if grouped:
                row.append(get_value(dw, "wagon_number", "") or "")
                row.append(get_value(dw, "type_wagon", "") or "")
            else:
                row.append(get_value(dw, "wagon_number_display", "") or "")
                row.append(get_value(dw, "type_wagon_display", "") or "")

        if grouped:
            row.extend(
                [
                    get_value(dw, "total_amount", 0) or 0,
                    get_value(dw, "total_time", 0) or 0,
                    get_value(dw, "total_price", 0) or 0,
                ]
            )
            if month_group:
                row.extend(
                    [get_value(dw, "month", "") or "", get_value(dw, "year", "") or ""]
                )
            else:
                row.append(get_value(dw, "year", "") or "")

        else:
            row.extend(
                [
                    get_value(dw, "amount", 0) or 0,
                    get_value(dw, "amount_time", 0) or 0,
                    get_value(dw, "amount_price", 0) or 0,
                    get_value(dw, "work_date", "") or "",
                ]
            )

        yield row
