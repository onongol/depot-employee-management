from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from employee.utils.pagination import paginate_queryset
from employee.utils.permissions import is_admin
from .wagon_filtered import wagon_filter
from .wagon_grouping import get_grouped_wagon_data, get_totals


@user_passes_test(is_admin, login_url='login')
@login_required(login_url='login')
def wagon_list(request):
    """
    View to list all wagons with related works, amount, total time, price, and date.
    Aggregates piecework records by wagon, work, date, and group.
    For each group, amount is taken as the maximum value (not summed), 
    while price is summed for all records in the group.
    """

    # Get filter parameters from GET request
    # Get the selected department from the request/session
    dailyworks, wagon_number, work_name, work_date, department = wagon_filter(request)

    # Aggregate dailywork data by wagon, work, date, and group_id
    wagon_data = get_grouped_wagon_data(dailyworks)

    # Paginate the aggregated data for the template
    page_obj = paginate_queryset(request, wagon_data)

    # Calculate totals
    totals = get_totals(dailyworks)

    # Render the wagon list template with grouped data
    return render(
        request,
        'wagon/wagon_list.html',
        {
            'wagon_data': wagon_data,
            'page_obj': page_obj,
            'selected_wagon': wagon_number,
            'selected_department': department,
            'total_amount': totals['total_amount'],
            'total_time': totals['total_time'],
            'total_price': totals['total_price'],
        }
    )
