from django.db.models import Q
from datetime import datetime

from employee.models import Piecework
from employee.utils.filters import filter_material
from employee.utils.converting_date import parse_date


def materials_prepare(request):
    """Prepare the base queryset and filter parameters for materials."""
    # Filtering parameters from request
    work_name = request.GET.get('work_name')
    selected_type = request.GET.get('type_material', 'all')
    start_date = parse_date(request.GET.get('start_date'))
    end_date = parse_date(request.GET.get('end_date'))

    # Prepare base queryset: exclude records where material is not used or not set
    pieceworks = Piecework.objects.exclude(
        Q(work__type_material__isnull=True) |
        Q(work__type_material="Not used") |
        Q(work__usage_material=0)
    )

    return pieceworks, work_name, selected_type, start_date, end_date


def materials_filtered(request):
    """Filtered materials data for export."""
    # Prepare the base queryset and filter parameters
    pieceworks, work_name, selected_type, start_date, end_date = materials_prepare(request)
    
    # Apply reusable filter for materials
    pieceworks = filter_material(
        pieceworks,
        work_name=work_name,
        selected_type=selected_type,
        start_date=start_date,
        end_date=end_date
    )

    return pieceworks
