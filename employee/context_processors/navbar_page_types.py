def navbar_page_types(request):
    """Provide a list of url_names requiring special navbar layout."""
    special_pages = {
        "employee_create",
        "employee_update",
        "daily_work_create",
        "daily_work_update",
        "daily_salary_create",
        "daily_salary_update",
    }

    back_pages = {
        "daily_work_create",
    }

    url_name = getattr(getattr(request, "resolver_match", None), "url_name", None)

    return {
        "navbar_page_types": special_pages,
        "is_special_navbar": url_name in special_pages,
        "is_back_pages": url_name in back_pages,
    }
