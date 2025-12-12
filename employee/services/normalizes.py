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

def normalize_wagon_number(wagon_number: Optional[str]) -> Optional[str]:
    """Normalize wagon_number: return None if empty or only whitespace."""
    if not wagon_number:
        return None
    return wagon_number.strip() or None


def normalize_job_title(current: Optional[str], obj) -> Optional[str]:
    """Return current job_title if provided, else take from Work."""
    return current or getattr(obj, "job_title", None)


def normalize_type_wagon(obj) -> Optional[str]:
    """Keep work.type_wagon if present, else None."""
    return getattr(obj, "type_wagon", None) or None
