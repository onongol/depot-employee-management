"""
Normalization helpers for cleaning and stabilizing domain fields.

These functions:
- Convert empty/whitespace inputs to None (e.g., wagon_number).
- Resolve missing values from related objects (e.g., job_title from Work).
- Enforce consistent optional fields (e.g., type_wagon set to None when absent).

Use them in model save/clean methods to keep data consistent, reduce edge cases,
and simplify downstream reporting and validation.
"""

from typing import Optional


def normalize_field(current: Optional[str], obj, attr_name: str) -> Optional[str]:
    """Return current if provided, else take attr_name from obj."""
    return current or getattr(obj, attr_name, None)


def normalize_str_field(value: Optional[str]) -> Optional[str]:
    """Normalize string field: return None if empty or only whitespace, else stripped value."""
    if not value:
        return None
    return value.strip() or None
