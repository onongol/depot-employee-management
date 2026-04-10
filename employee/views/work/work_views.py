from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView

from employee.forms import UpdateWorkForm, WorkForm
from employee.mixins.context_mixins import WorkContextMixin
from employee.mixins.create_mixin import AdminLoggedCreateMixin
from employee.mixins.department_form_mixins import FormDepartmentMixin
from employee.mixins.department_mixins import InitialDepartmentMixin
from employee.mixins.mechanic_context_mixins import MechanicContextMixin
from employee.mixins.permissions_mixins import OnlyAdminMixin
from employee.mixins.update_mixin import AdminLoggedUpdateMixin
from employee.mixins.wagon_context_mixins import WagonContextMixin


class WorkCreateView(
    LoginRequiredMixin,
    OnlyAdminMixin,
    WorkContextMixin,
    WagonContextMixin,
    MechanicContextMixin,
    SuccessMessageMixin,
    FormDepartmentMixin,
    InitialDepartmentMixin,
    AdminLoggedCreateMixin,
    CreateView,
):
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
    MechanicContextMixin,
    SuccessMessageMixin,
    FormDepartmentMixin,
    InitialDepartmentMixin,
    AdminLoggedUpdateMixin,
    UpdateView,
):
    form_class = UpdateWorkForm
    template_name = "work/work_update.html"
    success_message = _("Updated")
