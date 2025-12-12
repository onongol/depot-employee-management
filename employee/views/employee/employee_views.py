from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, UpdateView

from employee.forms import EmployeeForm, UpdateEmployeeForm
from employee.mixins.block_delete_mixins import BlockDeleteMixin
from employee.mixins.context_mixins import EmployeeContextMixin
from employee.mixins.delete_protection_mixins import DeleteProtectionMixin
from employee.mixins.department_mixins import InitialDepartmentMixin
from employee.models import DailySalary
from employee.utils.permissions import OnlyAdminMixin


class EmployeeCreateView(LoginRequiredMixin, OnlyAdminMixin, EmployeeContextMixin, InitialDepartmentMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    form_class = EmployeeForm
    template_name = "employee/employee_create.html"
    success_message = _("Employee %(employee_id)s/%(name)s created successfully.")


class EmployeeUpdateView(LoginRequiredMixin, OnlyAdminMixin, EmployeeContextMixin, InitialDepartmentMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    form_class = UpdateEmployeeForm
    template_name = "employee/employee_update.html"
    success_message = _("Employee updated successfully.")


class EmployeeDeleteView(LoginRequiredMixin, OnlyAdminMixin, EmployeeContextMixin, BlockDeleteMixin, DeleteProtectionMixin, DeleteView):
    login_url = 'login'
    template_name = "employee/employee_confirm_delete.html"
    block_related_models = [_('Daily Salary'), _('Daily Work'), _('Piecework')]

    # Get related daily salary records to check if deletion is allowed.
    def get_related_objects(self):
        return DailySalary.objects.filter(employee=self.object)
  
    def get_redirect_url(self):
        return self.success_url

    def get_object_name(self):
        return f"{self.object.employee_id}/{self.object.name}"
