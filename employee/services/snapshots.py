def snapshot_attr(obj, attr):
    """Return obj.attr snapshot for denormalization, or None if unavailable."""
    try:
        return getattr(obj, attr, None)
    except Exception:
        return None
