from django.contrib.auth.decorators import login_required, permission_required

from employee.views.daily_work.daily_work_create.daily_work_piecework_create import (
    daily_work_piecework_create,
)


@login_required
@permission_required("employee.add_piecework")
def piecework_create(request):
    """View to create new piecework records."""
    return daily_work_piecework_create(request)
