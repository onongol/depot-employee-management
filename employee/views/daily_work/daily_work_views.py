from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from employee.forms.daily_work_forms import UpdateDailyWorkForm
from employee.mixins.context_mixins import DailyWorkContextMixin
from employee.mixins.department_form_mixins import FormDepartmentMixin
from employee.mixins.update_mixin import AdminLoggedUpdateMixin
from employee.models.daily_work_models import DailyWork
from employee.views.daily_work.daily_work_create.daily_work_piecework_create import (
    daily_work_piecework_create,
)


class DailyWorkUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DailyWorkContextMixin,
    SuccessMessageMixin,
    FormDepartmentMixin,
    AdminLoggedUpdateMixin,
    UpdateView,
):
    permission_required = "employee.change_dailywork"
    queryset = DailyWork.objects.select_related("work")
    form_class = UpdateDailyWorkForm
    template_name = "daily_work/daily_work_piecework_update.html"
    success_message = _("Updated")


@login_required
@permission_required("employee.add_dailywork", raise_exception=True)
def daily_work_create(request):
    """Create daily work entry view. Redirect to piecework creation if department allows wagon work."""
    return daily_work_piecework_create(request)
