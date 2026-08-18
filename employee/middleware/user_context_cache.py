from employee.utils.request_department import (
    get_selected_department_from_request,
)


class UserContextCacheMiddleware:
    """Caches the selected department on the request for the duration of the request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        get_selected_department_from_request(request)

        response = self.get_response(request)
        return response
