def snapshot_attr(obj, attr):
    """Return obj.attr snapshot for denormalization, or None if unavailable."""
    return getattr(obj, attr, None)
