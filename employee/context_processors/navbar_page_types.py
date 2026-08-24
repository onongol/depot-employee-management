SPECIAL_PAGES = frozenset(
    {
        "employee_create",
        "employee_update",
        "work_create",
        "work_update",
        "daily_work_create",
        "daily_work_update",
        "daily_salary_create",
        "daily_salary_update",
    }
)

BACK_PAGES = frozenset(
    {
        "daily_work_create",
    }
)


def navbar_page_types(request):
    """Provide a list of url_names requiring special navbar layout."""
    special_pages = SPECIAL_PAGES

    back_pages = BACK_PAGES

    url_name = getattr(getattr(request, "resolver_match", None), "url_name", None)

    return {
        "is_special_navbar": url_name in special_pages,
        "is_back_pages": url_name in back_pages,
    }
