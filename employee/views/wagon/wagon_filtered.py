from django.db.models import Q
from django.db.models import Sum, F, FloatField, ExpressionWrapper, Max

from employee.models import Piecework
from employee.utils.filters import filter_wagon


def wagon_prepare(request):
    """Prepare the base queryset and filter parameters for wagons."""
    wagon_number = request.GET.get('wagon_number', '').strip()
    work_name = request.GET.get('work')
    work_date = request.GET.get('work_date')

    pieceworks = Piecework.objects.select_related('work').filter(
        employee__is_active=True,
    ).exclude(wagon_number__isnull=True).exclude(wagon_number='0')

    return pieceworks, wagon_number, work_name, work_date


def wagon_filtered(request):
    """Filtered wagon data for export."""
    pieceworks, wagon_number, work_name, work_date = wagon_prepare(request)

    pieceworks = filter_wagon(
        pieceworks,
        wagon_number=wagon_number,
        work_name=work_name,
        work_date=work_date
    )

    return pieceworks


def wagon_list(request):
    """
    View to list all wagons with related works, amount, total time, price, and date.
    """
    pieceworks = wagon_prepare(request)

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

    return wagon_data