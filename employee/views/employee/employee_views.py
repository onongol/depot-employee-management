from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView

from employee.forms import EmployeeForm, UpdateEmployeeForm
from employee.mixins.context_mixins import EmployeeContextMixin
from employee.mixins.create_mixin import AdminLoggedCreateMixin
from employee.mixins.department_mixins import InitialDepartmentMixin
from employee.mixins.permissions_mixins import OnlyPayrollsMixin
from employee.mixins.update_mixin import AdminLoggedUpdateMixin


class EmployeeCreateView(
    LoginRequiredMixin,
    OnlyPayrollsMixin,
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
    OnlyPayrollsMixin,
    EmployeeContextMixin,
    InitialDepartmentMixin,
    SuccessMessageMixin,
    AdminLoggedUpdateMixin,
    UpdateView,
):
    form_class = UpdateEmployeeForm
    template_name = "employee/employee_update.html"
    success_message = _("Updated")
