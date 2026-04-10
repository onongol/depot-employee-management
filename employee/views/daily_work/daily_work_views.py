from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from employee.forms.daily_work_forms import UpdateDailyWorkForm
from employee.mixins.context_mixins import DailyWorkContextMixin
from employee.mixins.department_form_mixins import FormDepartmentMixin
from employee.mixins.permissions_mixins import OnlyAdminMixin
from employee.mixins.update_mixin import AdminLoggedUpdateMixin
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
    AdminLoggedUpdateMixin,
    UpdateView,
):
    form_class = UpdateDailyWorkForm
    template_name = "daily_work/daily_work_piecework_update.html"
    success_message = _("Updated")


@login_required
@user_passes_test(is_creater)
def daily_work_create(request):
    """Create daily work entry view. Redirect to piecework creation if department allows wagon work."""
    return daily_work_piecework_create(request)
