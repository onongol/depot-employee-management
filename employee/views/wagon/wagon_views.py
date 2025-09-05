from django.shortcuts import render
from django.db.models import Sum, F, FloatField, ExpressionWrapper, Max
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from collections import defaultdict

from employee.models import Piecework
from employee.utils.select_department import get_selected_department
from .wagon_filtered import wagon_prepare
from employee.utils.filters import filter_wagon
from employee.utils.pagination import paginate_queryset
from employee.utils.permissions import is_admin


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
    pieceworks, wagon_number, work_name, work_date = wagon_prepare(request)

    # Apply wagon_number,  work name, work date filter if provided
    pieceworks = filter_wagon(
        pieceworks,
        wagon_number=wagon_number,
        work_name=work_name,
        work_date=work_date
    )

    # Aggregate piecework data by wagon, work, date, and group_id
    # amount: take the maximum value in the group (do not sum)
    # total_price: sum all prices in the group
    # total_time: calculated as standard_time * amount
    wagon_data = (
        pieceworks
        .values('type_work','wagon_number', 'work__work_name', 'work__standard_time', 'work_date', 'group_id')
        .annotate(
            amount=Max('amount'),  # Only one amount per group (not summed)
            total_price=Sum('amount_price'),  # Sum price for all records in the group
        )
        .annotate(
            total_time=ExpressionWrapper(
                F('work__standard_time') * F('amount'),
                output_field=FloatField()
            ),
        )
        .order_by('-work_date', 'type_work', 'wagon_number', 'work__work_name', 'group_id')
    )

    # Paginate the aggregated data for the template
    page_obj = paginate_queryset(request, wagon_data)

    # Group and sum by wagon_number, work__work_name, work_date
    grouped = defaultdict(lambda: {'amount': 0, 'total_price': 0, 'total_time': 0})
    for row in page_obj.object_list:
        key = (row['wagon_number'], row['work__work_name'], row['work_date'], row['type_work'])
        grouped[key]['amount'] += row['amount']
        grouped[key]['total_price'] += row['total_price']
        grouped[key]['total_time'] += row['total_time']

    # Convert grouped dict to list for template
    grouped_wagon_data = [
        {
            'wagon_number': k[0],
            'work__work_name': k[1],
            'work_date': k[2],
            'type_work': k[3],
            'amount': v['amount'],
            'total_price': v['total_price'],
            'total_time': v['total_time'],
        }
        for k, v in grouped.items()
    ]

    # Calculate totals for the current page (after grouping)
    total_amount = sum(row['amount'] for row in grouped_wagon_data)
    total_time = sum(row['total_time'] for row in grouped_wagon_data)
    total_price = sum(row['total_price'] for row in grouped_wagon_data)

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
