from employee.utils.get_value import get_value


def iter_rows(qs, context):
    show_wagon = context.show_wagon
    month_group = context.month_group
    year_group = context.year_group
    grouped = month_group or year_group

    for i, pw in enumerate(qs, start=1):
        # Snapshot/values keys used by grouped queries
        employee_id = get_value(pw, "employee_id", "") or ""
        employee_name = get_value(pw, "employee_name", "") or ""
        department_val = get_value(pw, "department", "") or ""
        job_title = get_value(pw, "job_title", "") or ""
        work_name = get_value(pw, "work_name", "") or ""
        type_work = get_value(pw, "type_work", "") or ""

        # For non-grouped (model instances), fall back to related objects if needed
        if not grouped:
            employee_id = (
                employee_id
                or getattr(getattr(pw, "employee", None), "employee_id", "")
                or ""
            )
            employee_name = (
                employee_name
                or getattr(getattr(pw, "employee", None), "name", "")
                or ""
            )
            department_val = department_val or getattr(pw, "department", "") or ""
            work_name = (
                work_name or getattr(getattr(pw, "work", None), "work_name", "") or ""
            )

        row = [
            i,
            employee_id,
            employee_name,
            department_val,
            job_title,
            work_name,
            type_work,
        ]

        if show_wagon:
            if grouped:
                row.append(get_value(pw, "wagon_number", "") or "")
                row.append(get_value(pw, "type_wagon", "") or "")
            else:
                row.append(get_value(pw, "wagon_number_display", "") or "")
                row.append(get_value(pw, "type_wagon_display", "") or "")

        if grouped:
            row.extend(
                [
                    get_value(pw, "total_amount", 0) or 0,
                    get_value(pw, "total_time", 0) or 0,
                    get_value(pw, "total_price", 0) or 0,
                ]
            )
            if month_group:
                row.extend(
                    [get_value(pw, "month", "") or "", get_value(pw, "year", "") or ""]
                )
            else:
                row.append(get_value(pw, "year", "") or "")

        else:
            row.extend(
                [
                    get_value(pw, "amount", 0) or 0,
                    get_value(pw, "amount_time", 0) or 0,
                    get_value(pw, "amount_price", 0) or 0,
                    get_value(pw, "work_date", "") or "",
                ]
            )

        yield row
