PAGES_REQUIRING_DEPARTMENT = frozenset(
    {
        "employee_list",
        "work_list",
        "daily_salary_list",
        "daily_work_list",
        "piecework_list",
        "employee_salary_list",
        "wagon_list",
    }
)


def needs_department_warning(request):
    """Provide a flag when selected_department is empty and current page needs a department."""

    url_name = getattr(getattr(request, "resolver_match", None), "url_name", None)

    selected_department = request.GET.get("department")
    if selected_department is None:
        selected_department = request.session.get("department")
    selected_department = (
        selected_department.strip()
        if isinstance(selected_department, str)
        else selected_department
    )

    return {
        "needs_department_warning": (not selected_department)
        and (url_name in PAGES_REQUIRING_DEPARTMENT)
    }
