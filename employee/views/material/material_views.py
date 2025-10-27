from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, user_passes_test

from .material_filtered import material_prepare, group_and_sum_materials
from employee.utils.filters import filter_material
from employee.utils.pagination import paginate_queryset
from employee.utils.permissions import is_admin


@user_passes_test(is_admin, login_url='login')
@login_required(login_url='login')
def material_list(request):
    """View for calculating and listing material usage in piecework records,
    with filtering and pagination."""

    # Prepare the base queryset and filter parameters
    daily_works, work_name, selected_type, range_date = material_prepare(request)

    # Get all distinct type_materials for dropdown filter
    type_materials = daily_works.values_list('work__type_material', flat=True).distinct()

    # Apply reusable filter function
    daily_works = filter_material(
        daily_works,
        work_name=work_name,
        selected_type=selected_type,
        range_date=range_date
    )

    # Group and sum duplicate materials
    daily_works = group_and_sum_materials(daily_works)

    # Business logic: calculate the total amount of material used in the filtered queryset
    sum_amount = daily_works.aggregate(total=Sum('amount_material'))['total'] or 0
    
    # Paginate the queryset, default to last page if page not specified
    page_obj = paginate_queryset(request, daily_works)

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
        'daily_works': page_obj.object_list,
        'page_obj': page_obj,
        'filters': filters,
    }

    return render(request, 'material/material_list.html', context)
