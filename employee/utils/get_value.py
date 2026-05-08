from typing import Any


def get_value(item: Any, key: str, default: Any = "") -> Any:
    """Utility function to get a value from a dict or an object using a key."""
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)
