from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from django.shortcuts import render

from employee.utils.access import is_admin
from employee.utils.filters import filter_material
from employee.utils.pagination import paginate_queryset
from employee.utils.sorting import apply_ordering
from employee.views.material.material_grouping import group_and_sum_materials
from employee.views.material.material_prepare import material_prepare


@user_passes_test(is_admin, login_url="login")
@login_required(login_url="login")
def material_list(request):
    """View for calculating and listing material usage in piecework records,
    with filtering and pagination."""
    # Prepare the base queryset and filter parameters
    daily_works, work_name, type_material, range_date = material_prepare(request)

    # Get all distinct type_materials for dropdown filter
    type_materials = daily_works.values_list(
        "work__type_material", flat=True
    ).distinct()

    # Apply reusable filter function
    daily_works = filter_material(
        daily_works,
        work_name=work_name,
        type_material=type_material,
        range_date=range_date,
    )

    # Group and sum duplicate materials
    daily_works = group_and_sum_materials(daily_works)

    # Apply ordering based on request parameters
    order_by = request.GET.get("order_by")
    direction = request.GET.get("direction")

    daily_works = apply_ordering(
        daily_works,
        order_by,
        direction,
        allowed_fields=["work_date", "work__work_name", "work__type_material"],
        default="-work_date",
    )

    # Business logic: calculate the total amount of material used in the filtered queryset
    sum_amount = daily_works.aggregate(total=Sum("amount_material"))["total"] or 0

    # Paginate the queryset, default to last page if page not specified
    page_obj = paginate_queryset(request, daily_works)

    # Prepare filters for URL and template
    filters = {
        "work_name": work_name or "",
        "type_material": type_material or "",
        "range_date": range_date or "",
    }

    # Remove empty values for cleaner URLs
    filters = {k: v for k, v in filters.items() if v}

    context = {
        "work_name": work_name,
        "type_materials": type_materials,
        "type_material": type_material,
        "range_date": range_date,
        "sum_amount": sum_amount,
        "daily_works": page_obj.object_list,
        "page_obj": page_obj,
        "filters": filters,
    }

    return render(request, "material/material_list.html", context)
