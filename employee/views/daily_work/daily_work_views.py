from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView, UpdateView

from employee.forms.daily_work_forms import UpdateDailyWorkForm
from employee.mixins.context_mixins import DailyWorkContextMixin
from employee.mixins.delete_warning_mixins import DeleteWarningMixin
from employee.mixins.department_form_mixins import FormDepartmentMixin
from employee.mixins.permissions_mixins import OnlyAdminMixin
from employee.models import DailyWork
from employee.utils.access import is_creater
from employee.views.daily_work.daily_work_create.daily_work_piecework_create import (
    daily_work_piecework_create,
)


class DailyWorkUpdateView(
    LoginRequiredMixin,
    OnlyAdminMixin,
    DailyWorkContextMixin,
    SuccessMessageMixin,
    FormDepartmentMixin,
    UpdateView,
):
    login_url = "login"
    model = DailyWork
    form_class = UpdateDailyWorkForm
    template_name = "daily_work/daily_work_piecework_update.html"
    success_message = _("Updated")

    def get_success_url(self):
        return reverse("daily_work_list")


class DailyWorkDeleteView(
    LoginRequiredMixin,
    OnlyAdminMixin,
    DailyWorkContextMixin,
    DeleteWarningMixin,
    DeleteView,
):
    login_url = "login"
    model = DailyWork
    template_name = "daily_work/daily_work_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        """Handle the deletion of a DailyWork entry."""
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("daily_work_list")


@login_required(login_url="login")
@user_passes_test(is_creater, login_url="login")
def daily_work_create(request):
    """Create daily work entry view. Redirect to piecework creation if department allows wagon work."""
    return daily_work_piecework_create(request)
