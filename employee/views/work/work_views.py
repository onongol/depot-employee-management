from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, UpdateView

from employee.forms import UpdateWorkForm, WorkForm
from employee.mixins.block_delete_mixins import BlockDeleteMixin
from employee.mixins.context_mixins import WorkContextMixin
from employee.mixins.delete_protection_mixins import DeleteProtectionMixin
from employee.mixins.department_form_mixins import FormDepartmentMixin
from employee.mixins.department_mixins import InitialDepartmentMixin
from employee.mixins.permissions_mixins import OnlyAdminMixin
from employee.mixins.wagon_context_mixins import WagonContextMixin
from employee.models import Piecework


class WorkCreateView(
    LoginRequiredMixin,
    OnlyAdminMixin,
    WorkContextMixin,
    WagonContextMixin,
    SuccessMessageMixin,
    FormDepartmentMixin,
    InitialDepartmentMixin,
    CreateView,
):
    login_url = "login"
    form_class = WorkForm
    template_name = "work/work_create.html"
    success_message = _("Created %(object_name)s")

    def get_success_message(self, _cleaned_data):
        return self.success_message % {
            "object_name": self.get_object_name(self.object),
        }


class WorkUpdateView(
    LoginRequiredMixin,
    OnlyAdminMixin,
    WorkContextMixin,
    WagonContextMixin,
    SuccessMessageMixin,
    FormDepartmentMixin,
    InitialDepartmentMixin,
    UpdateView,
):
    login_url = "login"
    form_class = UpdateWorkForm
    template_name = "work/work_update.html"
    success_message = _("Updated")


class WorkDeleteView(
    LoginRequiredMixin,
    OnlyAdminMixin,
    WorkContextMixin,
    BlockDeleteMixin,
    DeleteProtectionMixin,
    DeleteView,
):
    login_url = "login"
    template_name = "work/work_confirm_delete.html"
    block_related_models = [_("Daily Work"), _("Piecework")]

    # Get related piecework records to check if deletion is allowed.
    def get_related_objects(self):
        return Piecework.objects.filter(work=self.object)

    # Handle the deletion and send a warning.
    def get_redirect_url(self):
        return self.success_url
