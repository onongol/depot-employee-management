from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _

from employee.models import Piecework
from employee.utils.select_department import get_selected_department
from employee.utils.filters import filter_pieceworks
from employee.utils.pagination import paginate_queryset
from employee.utils.sorting import apply_ordering
from employee.utils.selects import get_distinct_values
from employee.utils.select_type_wagon import get_type_wagon_filter_values
from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS


@login_required(login_url='login')
def piecework_list(request):
    """View to list all piecework records with filtering and pagination."""
    # Only show pieceworks for employees in the selected department
    department = get_selected_department(request)

    # If not an employee, show all pieceworks in the department
    if request.user.groups.filter(name='Employees').exists():
        pieceworks = Piecework.objects.select_related('employee', 'work').filter(
            employee__user=request.user, employee__department=department, employee__is_active=True
        )
    else:
        # If not an employee, show all pieceworks in the department
        pieceworks = Piecework.objects.select_related('employee', 'work').filter(employee__department=department, employee__is_active=True)

    # Get distinct values for filtering dropdown
    job_titles = get_distinct_values(Piecework, 'job_title', department, department_field='employee__department')
    type_works = get_distinct_values(Piecework, 'type_work', department, department_field='work__department')
    type_materials = get_distinct_values(Piecework, 'work__type_material', department, department_field='work__department')

    # Get snapshot values of type_wagon from Piecework
    type_wagons = get_type_wagon_filter_values(department, source_model='piecework')

    # Extract filter parameters from the request
    employee_id = request.GET.get('employee_id')
    employee_name = request.GET.get('employee_name')
    job_title = request.GET.get('job_title')
    work_name = request.GET.get('work_name')
    type_work = request.GET.get('type_work')
    wagon_number = request.GET.get('wagon_number')
    type_wagon = request.GET.get('type_wagon')
    type_material = request.GET.get('type_material')
    range_date = request.GET.get('range_date')
    record_date = request.GET.get('record_date')

    # Apply all filters using a reusable filter function
    pieceworks = filter_pieceworks(
        pieceworks,
        employee_id=employee_id,
        employee_name=employee_name,
        job_title=job_title,
        work_name=work_name,
        type_work=type_work,
        wagon_number=wagon_number,
        type_wagon=type_wagon,
        type_material=type_material,
        range_date=range_date,
        record_date=record_date
    )

    # Aggregation for totals
    totals = pieceworks.aggregate(
        total_amount=Sum('amount'),
        total_time=Sum('amount_time'),
        total_price=Sum('amount_price')
    )

    # Sorting
    order_by = request.GET.get('order_by')
    direction = request.GET.get('direction')

    pieceworks = apply_ordering(
        pieceworks, 
        order_by, 
        direction, 
        allowed_fields=['work_date', 'record_date'], 
        default=['-work_date', '-record_date']
    )

    # Paginate the results, 10 records per page
    page_obj = paginate_queryset(request, pieceworks)

    # Prepare current filter values for template context
    filters = {
        'employee_id': employee_id or '',
        'employee_name': employee_name or '',
        'job_title': job_title or '',
        'work_name': work_name or '',
        'type_work': type_work or '',
        'wagon_number': wagon_number or '',
        'type_wagon': type_wagon or '',
        'type_material': type_material or '',
        'range_date': range_date or '',
        'record_date': record_date or '',
    }

    # Render the template with all context data
    return render(
        request,
        'piecework/piecework_list.html',
        {   
            'employee_id': employee_id,
            'employee_name': employee_name,
            'job_title': job_title,
            'work_name': work_name,
            'type_work': type_work,
            'wagon_number': wagon_number,
            'type_wagon': type_wagon,
            'range_date': range_date,
            'record_date': record_date,
            'pieceworks': page_obj,
            'page_obj': page_obj,
            'selected_department': department,
            'type_works': type_works,
            'type_materials': type_materials,
            'job_titles': job_titles,
            'type_wagons': type_wagons,
            'ALLOWED_WAGON_DEPARTMENTS': ALLOWED_WAGON_DEPARTMENTS,
            'totals': totals,
            'filters': filters,
        }
    )
