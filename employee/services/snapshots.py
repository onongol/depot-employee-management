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
    