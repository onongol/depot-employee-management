from dataclasses import asdict

from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
from django.shortcuts import render

from employee.utils.filters import filter_material
from employee.utils.pagination import paginate_queryset
from employee.utils.sorting import apply_ordering
from employee.views.material.material_grouping import group_and_sum_materials
from employee.views.material.material_prepare import material_prepare


@login_required
@permission_required("employee.view_material_report")
def material_list(request):
    """View for calculating and listing material usage in piecework records,
    with filtering and pagination."""
    context = material_prepare(request)

    daily_works = context.daily_works

    daily_works = filter_material(daily_works, context=context)

    # Total material usage does not depend on presentation grouping.
    sum_amount = daily_works.aggregate(total=Sum("amount_material"))["total"] or 0

    # Group and sum duplicate materials
    daily_works = group_and_sum_materials(daily_works)

    daily_works = apply_ordering(
        daily_works,
        order_by=context.order_by,
        direction=context.direction,
        allowed_fields=["work_date", "work__work_name", "work__type_material"],
        default="-work_date",
    )

    page_obj = paginate_queryset(request, daily_works)

    return render(
        request,
        "material/material_list.html",
        {
            **asdict(context),
            "rows": page_obj.object_list,
            "page_obj": page_obj,
            "sum_amount": sum_amount,
        },
    )
