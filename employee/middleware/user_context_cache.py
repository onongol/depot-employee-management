from employee.utils.middleware_selected_department import (
    get_selected_department_from_request,
)
from employee.utils.user_roles import get_user_groups


class UserContextCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Middleware to cache user context department and groups for the duration of the request."""

        get_selected_department_from_request(request)

        if request.user.is_authenticated:
            get_user_groups(request)

        response = self.get_response(request)
        return response
