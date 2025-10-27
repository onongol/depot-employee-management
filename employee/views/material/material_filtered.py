from django.db.models import Q, Sum

from employee.models import DailyWork
from employee.utils.filters import filter_material


def material_prepare(request):
    """Prepare the base queryset and filter parameters for materials."""
    # Filtering parameters from request
    work_name = request.GET.get('work_name')
    selected_type = request.GET.get('type_material', '')
    range_date = request.GET.get('range_date')

    # Prepare base queryset: exclude records where material is not used or not set
    daily_works = DailyWork.objects.exclude(
        Q(work__type_material__isnull=True) |
        Q(work__type_material="Not used") |
        Q(work__usage_material=0)
    )

    return daily_works, work_name, selected_type, range_date


def material_filter(request):
    """Filtered materials data for export."""
    # Prepare the base queryset and filter parameters
    daily_works, work_name, selected_type, range_date = material_prepare(request)

    # Apply reusable filter for materials
    daily_works = filter_material(
        daily_works,
        work_name=work_name,
        selected_type=selected_type,
        range_date=range_date
    )

    return daily_works


def group_and_sum_materials(queryset):
    """
    Group and sum duplicate materials by date, work name, and material type.
    """
    return queryset.values(
        'work_date',
        'work__work_name',
        'work__type_material'
    ).annotate(
        amount_material=Sum('amount_material')
    ).order_by('-work_date', 'work__work_name', 'work__type_material')
