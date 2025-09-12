from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, user_passes_test

from .material_filtered import material_prepare
from employee.utils.filters import filter_material
from employee.utils.pagination import paginate_queryset
from employee.utils.permissions import is_admin
from employee.utils.sorting import apply_ordering


@user_passes_test(is_admin, login_url='login')
@login_required(login_url='login')
def material_list(request):
    """View for calculating and listing material usage in piecework records,
    with filtering and pagination."""
    # Prepare the base queryset and filter parameters
    pieceworks, work_name, selected_type, range_date = material_prepare(request)

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
    
    # Sorting
    order_by = request.GET.get('order_by')
    direction = request.GET.get('direction')

    pieceworks = apply_ordering(
        pieceworks, order_by, direction, allowed_fields=['work_date']
    )

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

    return render(request, 'material/material_list.html', context)
