def get_user_groups(request) -> set[str]:
    """Returns cached user groups for the current request."""
    if not hasattr(request, "_cached_user_groups"):
        request._cached_user_groups = set(
            request.user.groups.values_list("name", flat=True)
        )
    return request._cached_user_groups
