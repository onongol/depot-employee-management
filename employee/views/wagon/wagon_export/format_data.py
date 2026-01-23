def iter_rows(qs, month_group=None):
    for i, item in enumerate(qs, start=1):
        if month_group:
            row = [
                i,
                item.get("wagon_number") or "",
                item.get("type_wagon") or "",
                item.get("total_time") or 0,
                item.get("total_price") or 0,
                item.get("month") or "",
                item.get("year") or "",
            ]
        else:
            row = [
                i,
                item.get("wagon_number") or "",
                item.get("type_wagon") or "",
                item.get("work__work_name") or "",
                item.get("type_work") or "",
                item.get("amount") or 0,
                item.get("total_time") or 0,
                item.get("total_price") or 0,
                item.get("work_date") or "",
            ]
        yield row
