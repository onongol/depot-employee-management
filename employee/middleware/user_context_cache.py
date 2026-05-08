from employee.utils.request_department import (
    get_selected_department_from_request,
)
from employee.utils.user_roles import get_user_groups


class UserContextCacheMiddleware:
    """Caches user context (department and groups) for the duration of the request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:
            get_user_groups(request)

        get_selected_department_from_request(request)

        response = self.get_response(request)
        return response
