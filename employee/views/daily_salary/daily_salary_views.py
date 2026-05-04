from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from employee.forms import UpdateDailySalaryForm
from employee.mixins.context_mixins import DailySalaryContextMixin
from employee.mixins.permissions_mixins import OnlyAdminMixin
from employee.mixins.update_mixin import AdminLoggedUpdateMixin
from employee.models import DailySalary


class DailySalaryUpdateView(
    LoginRequiredMixin,
    OnlyAdminMixin,
    DailySalaryContextMixin,
    SuccessMessageMixin,
    AdminLoggedUpdateMixin,
    UpdateView,
):
    queryset = DailySalary.objects.select_related("employee")
    form_class = UpdateDailySalaryForm
    template_name = "daily_salary/daily_salary_update.html"
    success_message = _("Updated")
