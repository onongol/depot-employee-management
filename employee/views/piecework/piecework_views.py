from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView

from employee.mixins.context_mixins import PieceworkContextMixin
from employee.mixins.delete_warning_mixins import DeleteWarningMixin
from employee.mixins.permissions_mixins import OnlyAdminMixin
from employee.utils.access import is_creater


class PieceworkDeleteView(
    LoginRequiredMixin,
    OnlyAdminMixin,
    PieceworkContextMixin,
    DeleteWarningMixin,
    DeleteView,
):
    template_name = "piecework/piecework_delete.html"


@login_required()
@user_passes_test(is_creater)
def piecework_create(request):
    """View to create new piecework records."""
    # Circular import avoidance
    from employee.views.daily_work.daily_work_create.daily_work_piecework_create import (
        daily_work_piecework_create,
    )

    return daily_work_piecework_create(request)
