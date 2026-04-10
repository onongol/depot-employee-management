from django.contrib.auth.decorators import login_required, user_passes_test

from employee.utils.access import is_creater


@login_required
@user_passes_test(is_creater)
def piecework_create(request):
    """View to create new piecework records."""
    # Circular import avoidance
    from employee.views.daily_work.daily_work_create.daily_work_piecework_create import (
        daily_work_piecework_create,
    )

    return daily_work_piecework_create(request)
