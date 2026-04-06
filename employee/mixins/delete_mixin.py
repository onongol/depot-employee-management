from django.db import transaction
from django.http import HttpResponseRedirect

from employee.services.admin_log_entries import log_object_deletion


class AdminLoggedDeleteMixin:
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        with transaction.atomic():
            log_object_deletion(request.user, self.object)
            self.object.delete()

        return HttpResponseRedirect(success_url)
