from django.db import transaction

from employee.services.admin_log_entries import log_object_addition


class AdminLoggedCreateMixin:
    def form_valid(self, form):
        with transaction.atomic():
            response = super().form_valid(form)
            log_object_addition(self.request.user, self.object)
        return response
