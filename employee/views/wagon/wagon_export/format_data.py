def iter_rows(qs):
    """Generate rows for Employee Salary export based on department."""
    for i, item in enumerate(qs, start=1):
        row = [
            i,
            item['wagon_number'] or "",
            item['type_wagon'] or "",
            item['work__work_name'] or "",
            item['type_work'] or "",
            item['amount'] or 0,
            item['total_time'] or 0,
            item['total_price'] or 0,
            item['work_date'] or "",
        ]
        yield row
