from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from employee.utils.pagination import paginate_queryset
from employee.utils.permissions import is_admin
from employee.utils.filters import filter_wagon
from employee.utils.sorting import apply_ordering
from .wagon_prepare import wagon_prepare
from .wagon_aggregation import get_grouped_wagon_data, get_totals


@user_passes_test(is_admin, login_url='login')
@login_required(login_url='login')
def wagon_list(request):
    """
    View to list all wagons with related works, amount, total time, price, and date.
    Aggregates piecework records by wagon, work, date, and group.
    For each group, amount is taken as the maximum value (not summed), 
    while price is summed for all records in the group.
    """

    # Get the selected department from the request/session
    dailyworks, wagon_number, type_wagon, work_name, type_work, range_date, department = wagon_prepare(request)

    # Get distinct type_wagon and type_work for filter options
    type_wagons = dailyworks.values_list('type_wagon', flat=True).distinct()

    type_works = dailyworks.values_list('type_work', flat=True).distinct()

    # Apply filters based on request parameters
    dailyworks = filter_wagon(
        dailyworks,
        wagon_number=wagon_number,
        type_wagon=type_wagon,
        work_name=work_name,
        type_work=type_work,
        range_date=range_date
    )

    # Aggregate dailywork data by wagon, work, date, and group_id
    wagon_data = get_grouped_wagon_data(dailyworks)

    # Sorting
    order_by = request.GET.get('order_by')
    direction = request.GET.get('direction')
    
    wagon_data = apply_ordering(
        wagon_data,
        order_by,
        direction,
        allowed_fields=['work_date', 'work__work_name', 'type_work', 'wagon_number', 'type_wagon'],
        default='-work_date'
    )
    
    # Paginate the aggregated data for the template
    page_obj = paginate_queryset(request, wagon_data)

    # Calculate totals
    totals = get_totals(dailyworks)

    # Prepare filters for the template
    filters = {
        'wagon_number': wagon_number or '',
        'type_wagon': type_wagon or '',
        'work_name': work_name or '',
        'type_work': type_work or '',
        'range_date': range_date or '',
        'department': department or '',
    }

    # Render the wagon list template with grouped data
    return render(
        request,
        'wagon/wagon_list.html',
        {   
            'wagon_number': wagon_number,
            'type_wagon': type_wagon,
            'work_name': work_name,
            'type_work': type_work,
            'range_date': range_date,
            'wagon_data': wagon_data,
            'page_obj': page_obj,
            'selected_wagon': wagon_number,
            'selected_department': department,
            'total_amount': totals['total_amount'],
            'total_time': totals['total_time'],
            'total_price': totals['total_price'],
            'type_wagons': type_wagons,
            'type_works': type_works,
            'filters': filters
        }
    )
