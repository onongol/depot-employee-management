from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView

from employee.mixins.context_mixins import PieceworkContextMixin
from employee.mixins.delete_warning_mixins import DeleteWarningMixin
from employee.mixins.permissions_mixins import OnlyAdminMixin
from employee.utils.access import  is_creater


class PieceworkDeleteView(LoginRequiredMixin, OnlyAdminMixin, PieceworkContextMixin, DeleteWarningMixin, DeleteView):
    login_url = 'login'
    template_name = "piecework/piecework_delete.html"

    # Handle the deletion and send a warning.
    def get_redirect_url(self):
        return self.success_url
    
    def get_object_name(self):
        return (
            f"{self.object.employee.employee_id}/{self.object.employee.name}/{self.object.work.work_name}/{self.object.type_work}/{self.object.work_date}"
        )


@login_required(login_url='login')
@user_passes_test(is_creater, login_url='login')
def piecework_create(request):
    """View to create new piecework records."""
    # Circular import avoidance
    from employee.views.daily_work.daily_work_create.daily_work_piecework_create import \
        daily_work_piecework_create

    return daily_work_piecework_create(request)
