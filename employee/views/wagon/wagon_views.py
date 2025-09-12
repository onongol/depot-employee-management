from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from employee.utils.select_department import get_selected_department
from employee.utils.pagination import paginate_queryset
from employee.utils.permissions import is_admin
from .wagon_filtered import wagon_filter
from .wagon_grouping import get_grouped_wagon_data, regroup_and_sum_wagon_data


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
    department = get_selected_department(request)

    # Get filter parameters from GET request
    pieceworks, wagon_number, work_name, work_date = wagon_filter(request)
    
    # Aggregate piecework data by wagon, work, date, and group_id
    wagon_data = get_grouped_wagon_data(pieceworks)

    # Paginate the aggregated data for the template
    page_obj = paginate_queryset(request, wagon_data)

    # Group and sum by wagon_number, work__work_name, work_date. Convert grouped dict to list for template
    grouped_wagon_data, total_amount, total_time, total_price = regroup_and_sum_wagon_data(page_obj.object_list)

    # Render the wagon list template with grouped data
    return render(
        request,
        'wagon/wagon_list.html',
        {
            'wagon_data': grouped_wagon_data,
            'page_obj': page_obj,
            'selected_wagon': wagon_number,
            'selected_department': department,
            'total_amount': total_amount,
            'total_time': total_time,
            'total_price': total_price,
        }
    )
