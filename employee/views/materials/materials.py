from django.shortcuts import render
from django.db.models import Sum

from .materials_filtered import materials_prepare
from employee.utils.filters import filter_material
from employee.utils.pagination import paginate_queryset


def materials(request):
    """View for calculating and listing material usage in piecework records,
    with filtering and pagination."""
    # Prepare the base queryset and filter parameters
    pieceworks, work_name, selected_type, range_date = materials_prepare(request)

    # Get all distinct type_materials for dropdown filter
    type_materials = pieceworks.values_list('work__type_material', flat=True).distinct()

    # Apply reusable filter function
    pieceworks = filter_material(
        pieceworks,
        work_name=work_name,
        selected_type=selected_type,
        range_date=range_date
    )

    # Business logic: calculate the total amount of material used in the filtered queryset
    sum_amount = pieceworks.aggregate(total=Sum('amount_material'))['total'] or 0
    
    # Sorting: order by work_date, default is descending
    order_by = request.GET.get('order_by')
    direction = request.GET.get('direction')

    if order_by in ['work_date']:
        if direction == 'desc':
            pieceworks = pieceworks.order_by(f"-{order_by}")
        else:
            pieceworks = pieceworks.order_by(order_by)
    else:
        # Default ordering if no valid order_by is provided
        pieceworks = pieceworks.order_by('-work_date')

    # Paginate the queryset, default to last page if page not specified
    page_obj = paginate_queryset(request, pieceworks)

    # Prepare filters for URL and template
    filters = {
        'work_name': work_name or '',
        'type_material': selected_type,
        'range_date': range_date or '',
    }

    # Remove empty values for cleaner URLs
    filters = {k: v for k, v in filters.items() if v}
    
    context = {
        'type_materials': type_materials,
        'selected_type': selected_type,
        'range_date': range_date,
        'sum_amount': sum_amount,   # Total material usage for current filter
        'pieceworks': page_obj.object_list,
        'page_obj': page_obj,
        'filters': filters,
    }

    return render(request, 'materials/materials.html', context)
