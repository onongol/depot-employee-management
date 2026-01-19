def preview_items(qs, count, limit=10):
    """Generates a preview list and summary tail for bulk action messages, limiting displayed items for user-friendly feedback."""
    items = [
        f"{ds.employee.employee_id}/{ds.employee.name} - {ds.salary_date}"
        for ds in qs[:limit]
    ]
    tail = "" if count <= limit else _(" … and %(n)s more") % {"n": count - limit}
    return items, tail
