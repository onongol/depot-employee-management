from employee.constants.constants import DEFAULT_WAGON_NUMBER


def iter_rows(qs, *, wagon_mode: bool = False):
    for i, item in enumerate(qs, start=1):
        row = [
            i,
            item["employee"].employee_id or "",
            item["employee"].name or "",
            item["employee"].department or "",
            item["employee"].job_title or "",
            item["employee"].rank or "",
        ]

        if wagon_mode:
            wagon = item.get("wagon_number")
            row.append(wagon if wagon else DEFAULT_WAGON_NUMBER)

        row += [
            item.get("total_piecework_time") or 0,
            item.get("total_piecework_amount") or 0,
            item.get("month") or "",
            item.get("year") or "",
        ]

        yield row
