from dataclasses import asdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from employee.constants.constants import (
    ALLOWED_WAGON_DEPARTMENTS,
    GROUP_MONTH,
    GROUP_YEAR,
)
from employee.utils.filters import filter_pieceworks
from employee.utils.pagination import paginate_queryset
from employee.utils.totals_for_group import calc_totals_for_group
from employee.views.piecework.group.group_and_sort import group_and_sort_pieceworks
from employee.views.piecework.piecework_prepare import piecework_prepare


@login_required
def piecework_list(request):
    """View to list all piecework records with filtering and pagination."""
    context = piecework_prepare(request)

    pieceworks = context.pieceworks

    pieceworks = filter_pieceworks(pieceworks, context=context)

    totals = calc_totals_for_group(
        pieceworks,
        context=context,
        date_field="work_date",
    )

    pieceworks = group_and_sort_pieceworks(pieceworks, context=context)

    page_obj = paginate_queryset(request, pieceworks)

    return render(
        request,
        "piecework/piecework_list.html",
        {
            **asdict(context),
            "rows": page_obj,
            "page_obj": page_obj,
            "totals": totals,
            "ALLOWED_WAGON_DEPARTMENTS": ALLOWED_WAGON_DEPARTMENTS,
            "GROUP_MONTH": GROUP_MONTH,
            "GROUP_YEAR": GROUP_YEAR,
        },
    )
