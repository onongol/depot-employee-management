from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView, UpdateView

from employee.forms import UpdateDailySalaryForm
from employee.mixins.block_message_mixins import BlockMessageMixin
from employee.mixins.context_mixins import DailySalaryContextMixin
from employee.mixins.delete_mixins import DeleteProtectionMixin
from employee.models import Piecework
from employee.utils.permissions import OnlyAdminMixin


class DailySalaryUpdateView(LoginRequiredMixin, OnlyAdminMixin, DailySalaryContextMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    form_class = UpdateDailySalaryForm
    template_name = "daily_salary/daily_salary_update.html"
    success_message = _("Daily Salary updated successfully.")


class DailySalaryDeleteView(LoginRequiredMixin, OnlyAdminMixin, DailySalaryContextMixin, BlockMessageMixin, DeleteProtectionMixin, DeleteView):
    login_url = 'login'
    template_name = "daily_salary/daily_salary_confirm_delete.html"
    block_related_models = [_('Daily Salary'), _('Piecework')]

    # Get related piecework records to check if deletion is allowed.
    def get_related_objects(self):
        return Piecework.objects.filter(
            employee=self.object.employee,
            work_date=self.object.salary_date
        )
        
    # Handle the deletion and send a warning.
    def get_redirect_url(self):
        return self.success_url
    
    def get_object_name(self):
        return (
            f"{self.object.employee.employee_id}/{self.object.employee.name}/{self.object.salary_date}"
        )
