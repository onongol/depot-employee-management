from django.shortcuts import render
from django.db.models import Sum
from django.core.paginator import Paginator
from datetime import datetime

from employee.models import Piecework


def materials(request):
    """View for calculating and listing material usage in piecework records,
    with filtering and pagination."""
    # Filtering
    selected_type = request.GET.get('type_material', 'all')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # If 'all' is selected, set selected_type to None and amount = 0 for filtering
    pieceworks_base = (
        Piecework.objects.exclude(work__type_material__isnull=True)
        .exclude(work__type_material="Not used")
        .exclude(work__usage_material=0)
    )

    # Get all distinct type_materials from Piecework's related Work model
    type_materials = pieceworks_base.values_list('work__type_material', flat=True).distinct()

    pieceworks = pieceworks_base

    if selected_type != 'all':
        pieceworks = pieceworks.filter(work__type_material=selected_type)
    if start_date:
        pieceworks = pieceworks.filter(work_date__gte=start_date)
    if end_date:
        pieceworks = pieceworks.filter(work_date__lte=end_date)

    sum_amount = pieceworks.aggregate(total=Sum('amount_material'))['total'] or 0
    
    # Order queryset by work_date based on sort parameter
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
    paginator = Paginator(pieceworks, 10)
    page_number = request.GET.get('page')
    if not page_number:
        page_number = paginator.num_pages  # last page

    page_obj = paginator.get_page(page_number)

    # Filter for the URL
    filters = {
        'type_material': selected_type,
        'start_date': start_date or '',
        'end_date': end_date or '',
    }

    # Remove empty values so URLs are clean
    filters = {k: v for k, v in filters.items() if v}

    # Convert date strings to datetime objects for comparison
    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        except ValueError:
            start_date = None   
    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            end_date = None
            
    context = {
        'type_materials': type_materials,
        'selected_type': selected_type,
        'start_date': start_date,
        'end_date': end_date,
        'sum_amount': sum_amount,
        'pieceworks': page_obj.object_list,
        'page_obj': page_obj,
        'filters': filters,
    }

    return render(request, 'materials/materials.html', context)
