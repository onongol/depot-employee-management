from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from employee.forms import UpdateDailySalaryForm
from employee.mixins.context_mixins import DailySalaryContextMixin
from employee.mixins.update_mixin import AdminLoggedUpdateMixin
from employee.models import DailySalary


class DailySalaryUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DailySalaryContextMixin,
    SuccessMessageMixin,
    AdminLoggedUpdateMixin,
    UpdateView,
):
    permission_required = "employee.change_dailysalary"
    form_class = UpdateDailySalaryForm
    template_name = "daily_salary/daily_salary_update.html"
    success_message = _("Updated")

    def get_queryset(self):
        return DailySalary.objects.for_user(self.request.user).select_related(
            "employee"
        )
