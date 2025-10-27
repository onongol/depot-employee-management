from django.db.models import Q, Sum

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
