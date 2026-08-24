def normalize_field(current: str | None, obj, attr: str) -> str | None:
    """Return current if provided, else take attr from obj."""
    return current or getattr(obj, attr, None) or None


def normalize_str_field(value: str | None) -> str | None:
    """Normalize string field: return None if empty or only whitespace, else stripped value."""
    if not value:
        return None
    return value.strip() or None
