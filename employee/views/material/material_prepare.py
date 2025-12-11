from django.db.models import Q

from employee.models import DailyWork


def material_prepare(request):
    """Prepare the base queryset and filter parameters for materials."""
    # Filtering parameters from request
    work_name = request.GET.get('work_name')
    type_material = request.GET.get('type_material')
    range_date = request.GET.get('range_date')

    # Prepare base queryset: exclude records where material is not used or not set
    daily_works = DailyWork.objects.exclude(
        Q(work__type_material__isnull=True) |
        Q(work__usage_material=0)
    )

    return daily_works, work_name, type_material, range_date
