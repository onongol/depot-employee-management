from django.contrib.auth.decorators import login_required, permission_required


@login_required
@permission_required("employee.add_piecework")
def piecework_create(request):
    """View to create new piecework records."""
    # Circular import avoidance
    from employee.views.daily_work.daily_work_create.daily_work_piecework_create import (
        daily_work_piecework_create,
    )

    return daily_work_piecework_create(request)
