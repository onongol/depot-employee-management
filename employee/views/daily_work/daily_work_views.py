from django.urls import reverse
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _

from employee.models import DailyWork
from employee.mixins.context_mixins import DailyWorkContextMixin
from employee.mixins.delete_mixins import DeleteWarningMixin
from employee.forms.daily_work_forms import UpdateDailyWorkForm
from employee.utils.permissions import OnlyAdminMixin, is_creater
from employee.utils.select_department import get_selected_department
from .daily_work_piecework_create import daily_work_piecework_create
from .daily_work_list import daily_work_list


class DailyWorkUpdateView(LoginRequiredMixin, OnlyAdminMixin, DailyWorkContextMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    model = DailyWork
    form_class = UpdateDailyWorkForm
    template_name = "daily_work/daily_work_piecework_update.html"
    success_message = _("Daily Work and Piecework updated successfully.")

    def get_form_kwargs(self):
        """Pass selected department to the form."""
        kwargs = super().get_form_kwargs()
        department = get_selected_department(self.request)
        kwargs['department'] = department
        return kwargs

    def get_success_url(self):
        return reverse('daily_work_list')
    

class DailyWorkDeleteView(LoginRequiredMixin, OnlyAdminMixin, DailyWorkContextMixin, DeleteWarningMixin, DeleteView):
    login_url = 'login'
    model = DailyWork
    template_name = "daily_work/daily_work_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        """Handle the deletion of a DailyWork entry."""
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('daily_work_list')
    
    def get_object_name(self):
        return (
            f"{self.object.work.work_name}/{self.object.type_work}/{self.object.work_date}"
        )


@login_required(login_url='login')
@user_passes_test(is_creater, login_url='login')
def daily_work_create(request):
    """Create daily work entry view. Redirect to piecework creation if department allows wagon work."""
    return daily_work_piecework_create(request)
