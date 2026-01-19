def parse_ids(raw_ids):
    """Handles bulk deletion of DailySalary via checkboxes, blocking deletions linked to Piecework, and displays user feedback messages."""
    ids = []
    for x in raw_ids:
        try:
            ids.append(int(x))
        except (TypeError, ValueError):
            continue
    return ids
