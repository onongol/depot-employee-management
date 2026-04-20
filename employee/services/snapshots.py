"""
Snapshot helpers for denormalizing related model fields at save time.

These functions safely read attributes (e.g., employee_name, department, work_name) from
related objects and persist them on the current record. This:
- Preserves historical values even if the related objects change later.
- Simplifies reporting/exports without extra JOINs.
- Avoids failures when related objects are deleted or fields become unavailable.
"""


def snapshot_attr(obj, attr_name):
    try:
        return getattr(obj, attr_name, None)
    except Exception:
        return None
