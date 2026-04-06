from django.db import transaction

from employee.services.admin_log_entries import log_object_change


class AdminLoggedUpdateMixin:
    def form_valid(self, form):
        with transaction.atomic():
            response = super().form_valid(form)
            log_object_change(
                self.request.user,
                self.object,
                changed_fields=form.changed_data,
            )
        return response
