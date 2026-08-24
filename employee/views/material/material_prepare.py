from django.db.models import Q

from employee.forms.filter_forms import DateRangeFilterForm
from employee.models import DailyWork
from employee.views.material.marerial_context import MaterialContext


def material_prepare(request) -> MaterialContext:
    """Prepare the base queryset and filter parameters for materials."""
    # Prepare base queryset: exclude records where material is not used or not set
    daily_works = DailyWork.objects.for_user(request.user).exclude(
        Q(work__type_material__isnull=True) | Q(work__usage_material=0)
    )

    work_name = request.GET.get("work_name")
    type_material = request.GET.get("type_material")

    # Dates are parsed here, at the edge; the filter only applies them.
    range_date = request.GET.get("range_date")
    date_from, date_to = DateRangeFilterForm.parse(request.GET).get("range_date") or (
        None,
        None,
    )

    order_by = request.GET.get("order_by")
    direction = request.GET.get("direction")

    return MaterialContext(
        daily_works=daily_works,
        work_name=work_name,
        type_material=type_material,
        range_date=range_date,
        date_from=date_from,
        date_to=date_to,
        order_by=order_by,
        direction=direction,
    )
