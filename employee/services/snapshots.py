"""
Snapshot helpers for denormalizing related model fields at save time.

These functions safely read attributes (e.g., name, department, work_name) from
related objects and persist them on the current record. This:
- Preserves historical values even if the related objects change later.
- Simplifies reporting/exports without extra JOINs.
- Avoids failures when related objects are deleted or fields become unavailable.
"""

def snapshot_employee_name(obj):
    try:
        return getattr(obj, 'name', None)
    except Exception:
        return None
    

def snapshot_work_name(obj):
    try:
        return getattr(obj, 'work_name', None)
    except Exception:
        return None
    

def snapshot_department(obj):
    try:
        return getattr(obj, 'department', None)
    except Exception:
        return None
    