from django.shortcuts import render
from django.db.models import Sum
from django.core.paginator import Paginator
from datetime import datetime

from employee.models import Work
from employee.models import Piecework


def calculation_materials(request):
    """View for calculating and listing material usage in piecework records,
    with filtering and pagination."""
    # Filtering
    # Get all distinct type_materials from Work model
    type_materials = (
        Work.objects.exclude(type_material__isnull=True)
        .values_list('type_material', flat=True)
        .distinct()
    )
    selected_type = request.GET.get('type_material', 'all')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # If 'all' is selected, set selected_type to None and amount = 0 for filtering
    pieceworks = Piecework.objects.exclude(work__type_material__isnull=True).exclude(work__usage_material=0)

    if selected_type != 'all':
        pieceworks = pieceworks.filter(work__type_material=selected_type)
    if start_date:
        pieceworks = pieceworks.filter(work_date__gte=start_date)
    if end_date:
        pieceworks = pieceworks.filter(work_date__lte=end_date)

    sum_amount = pieceworks.aggregate(total=Sum('amount_material'))['total'] or 0

    # Order queryset by work_date in descending order
    pieceworks = pieceworks.order_by('work_date')

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

    return render(request, 'calculation/calculation_materials.html', context)
