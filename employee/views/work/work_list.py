from dataclasses import asdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS, MECHANIC
from employee.utils.filters import filter_works
from employee.utils.pagination import paginate_queryset
from employee.utils.sorting import apply_ordering
from employee.views.work.work_prepare import work_prepare


@login_required(login_url="login")
def work_list(request):
    """View to list all works with filtering and pagination."""
    context = work_prepare(request)

    works = context.works

    works = filter_works(works, context=context)
    works = apply_ordering(
        works,
        context.order_by,
        context.direction,
        allowed_fields=["work_name"],
        default=["work_name"],
    )

    page_obj = paginate_queryset(request, works)

    return render(
        request,
        "work/work_list.html",
        {
            **asdict(context),
            "works": page_obj,
            "page_obj": page_obj,
            "ALLOWED_WAGON_DEPARTMENTS": ALLOWED_WAGON_DEPARTMENTS,
            "MECHANIC": MECHANIC,
        },
    )
