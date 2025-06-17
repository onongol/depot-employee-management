from django.db.models import Q

from employee.models import Piecework
from employee.utils.filters import filter_material


def materials_filtered(request):
    """Filtered materials data for export."""
    # Filtering (reuse logic from materials)
    selected_type = request.GET.get('type_material', 'all')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Prepare base queryset: exclude records where material is not used or not set
    pieceworks = Piecework.objects.exclude(
        Q(work__type_material__isnull=True) |
        Q(work__type_material="Not used") |
        Q(work__usage_material=0)
    )

    # Apply reusable filter for materials
    pieceworks = filter_material(
        pieceworks,
        selected_type=selected_type,
        start_date=start_date,
        end_date=end_date
    )

    return pieceworks
