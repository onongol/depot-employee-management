from django.db.models import Q

from employee.models import DailyWork
from employee.views.material.marerial_context import MaterialContext


def material_prepare(request) -> MaterialContext:
    """Prepare the base queryset and filter parameters for materials."""
    # Prepare base queryset: exclude records where material is not used or not set
    daily_works = DailyWork.objects.exclude(
        Q(work__type_material__isnull=True) | Q(work__usage_material=0)
    )

    work_name = request.GET.get("work_name")
    type_material = request.GET.get("type_material")
    range_date = request.GET.get("range_date")

    order_by = request.GET.get("order_by")
    direction = request.GET.get("direction")

    return MaterialContext(
        daily_works=daily_works,
        work_name=work_name,
        type_material=type_material,
        range_date=range_date,
        order_by=order_by,
        direction=direction,
    )
