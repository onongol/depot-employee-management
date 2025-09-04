from django.shortcuts import render
from django.db.models import Sum, F, FloatField, ExpressionWrapper, Max
from django.contrib.auth.decorators import login_required

from employee.models import Piecework
from employee.utils.select_department import get_selected_department
from employee.utils.pagination import paginate_queryset


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
    wagon_number = request.GET.get('wagon_number', '').strip()
    work = request.GET.get('work')
    work_date = request.GET.get('work_date')

    # Build the base queryset: only active employees, with valid wagon_number
    pieceworks = Piecework.objects.select_related('work').filter(
        employee__department=department,
        employee__is_active=True,
    ).exclude(wagon_number__isnull=True).exclude(wagon_number='0')

    # Apply wagon_number,  work name, work date filter if provided
    if wagon_number:
        pieceworks = pieceworks.filter(wagon_number=wagon_number)
    if work:
        pieceworks = pieceworks.filter(work__work_name__icontains=work)
    if work_date:
        pieceworks = pieceworks.filter(work_date=work_date)

    # Aggregate piecework data by wagon, work, date, and group_id
    # amount: take the maximum value in the group (do not sum)
    # total_price: sum all prices in the group
    # total_time: calculated as standard_time * amount
    wagon_data = (
        pieceworks
        .values('wagon_number', 'work__work_name', 'work__standard_time', 'work_date', 'group_id')
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
        .order_by('-work_date', 'wagon_number', 'work__work_name', 'group_id')
    )

    # Paginate the aggregated data for the template
    page_obj = paginate_queryset(request, wagon_data)

    # Calculate totals for the current page
    total_time = sum(row['total_time'] for row in page_obj.object_list)
    total_price = sum(row['total_price'] for row in page_obj.object_list)

    # Render the wagon list template with aggregated data and filters
    return render(
        request,
        'wagon/wagon_list.html',
        {
            'wagon_data': page_obj,
            'page_obj': page_obj,
            'selected_wagon': wagon_number,
            'selected_department': department,
            'total_time': total_time,
            'total_price': total_price,
        }
    )
