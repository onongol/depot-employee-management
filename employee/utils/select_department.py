from employee.constants.constants import DEPARTMENTS


def get_selected_department(request):
    """Return the validated selected department cached on the request."""
    department = getattr(request, "selected_department", None)
    if department is not None:
        return department

    raw_department = request.GET.get("department")
    return raw_department if raw_department in DEPARTMENTS else None
