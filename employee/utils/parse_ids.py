def parse_ids(raw_ids) -> list[int]:
    """Parse a list of raw values into a list of integers, skipping invalid entries."""
    ids = []
    for x in raw_ids:
        try:
            ids.append(int(x))
        except (TypeError, ValueError):
            continue
    return ids
