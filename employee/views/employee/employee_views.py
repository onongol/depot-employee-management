from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, UpdateView

from employee.forms import EmployeeForm, UpdateEmployeeForm
from employee.mixins.block_delete_mixins import BlockDeleteMixin
from employee.mixins.context_mixins import EmployeeContextMixin
from employee.mixins.create_mixin import AdminLoggedCreateMixin
from employee.mixins.delete_mixin import AdminLoggedDeleteMixin
from employee.mixins.delete_protection_mixins import DeleteProtectionMixin
from employee.mixins.department_mixins import InitialDepartmentMixin
from employee.mixins.permissions_mixins import OnlyAdminMixin
from employee.mixins.update_mixin import AdminLoggedUpdateMixin
from employee.models import DailySalary


class EmployeeCreateView(
    LoginRequiredMixin,
    OnlyAdminMixin,
    EmployeeContextMixin,
    InitialDepartmentMixin,
    SuccessMessageMixin,
    AdminLoggedCreateMixin,
    CreateView,
):
    form_class = EmployeeForm
    template_name = "employee/employee_create.html"
    success_message = _("Created %(object_name)s")

    def get_success_message(self, _cleaned_data):
        return self.success_message % {
            "object_name": self.get_object_name(self.object),
        }


class EmployeeUpdateView(
    LoginRequiredMixin,
    OnlyAdminMixin,
    EmployeeContextMixin,
    InitialDepartmentMixin,
    SuccessMessageMixin,
    AdminLoggedUpdateMixin,
    UpdateView,
):
    form_class = UpdateEmployeeForm
    template_name = "employee/employee_update.html"
    success_message = _("Updated")


class EmployeeDeleteView(
    LoginRequiredMixin,
    OnlyAdminMixin,
    EmployeeContextMixin,
    BlockDeleteMixin,
    DeleteProtectionMixin,
    AdminLoggedDeleteMixin,
    DeleteView,
):
    template_name = "employee/employee_confirm_delete.html"
    block_related_models = [_("Daily Salary"), _("Daily Work"), _("Piecework")]

    # Get related daily salary records to check if deletion is allowed.
    def get_related_objects(self):
        return DailySalary.objects.filter(employee=self.object)
