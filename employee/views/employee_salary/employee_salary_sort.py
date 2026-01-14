def apply_ordering(rows, order_by, direction, *, allowed_fields):
    """
    Sort a list[dict] in memory in a similar way to apply_ordering() for QuerySets.

    - rows: list of dicts (e.g., employee_salaries)
    - order_by: field name to sort by (str)
    - direction: 'asc' or 'desc'
    - allowed_fields: whitelist of sortable fields
    - default_key: key function used for the default sort order
    """
    reverse = (direction == "desc")

    if order_by not in allowed_fields:
        rows.sort(key=lambda x: (x.get("year") or 0, x.get("month") or 0), reverse=True)
        return rows

    if order_by == "employee_id":
        rows.sort(key=lambda x: (x["employee"].employee_id or 0), reverse=reverse)
        return rows

    rows.sort(key=lambda x: (x.get("year") or 0, x.get("month") or 0), reverse=reverse)
    return rows
