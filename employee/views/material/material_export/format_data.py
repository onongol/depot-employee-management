def iter_rows(qs):
    for i, item in enumerate(qs, start=1):
        row = [
            i,
            item["work__type_material"] or "",
            item["work__work_name"] or "",
            item["amount_material"] or 0,
            item["work_date"] or "",
        ]
        yield row
