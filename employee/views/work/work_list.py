from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS
from employee.models import Work
from employee.utils.filters import filter_works
from employee.utils.pagination import paginate_queryset
from employee.utils.select_department import get_selected_department
from employee.utils.select_type_wagon import get_type_wagon_filter_values
from employee.utils.selects import get_distinct_values


@login_required(login_url='login')
def work_list(request):
    """View to list all works with filtering and pagination."""
    works = Work.objects.all()

    # Extract filter parameters from the request
    department = get_selected_department(request)
    job_title = request.GET.get('job_title')
    work_name = request.GET.get('work_name')
    type_wagon = request.GET.get('type_wagon')

    # Apply all filters using a reusable filter function
    works = filter_works(
        works, 
        department=department,
        job_title=job_title,
        work_name=work_name,
        type_wagon=type_wagon,
    )

    # Get distinct job titles for filtering dropdown
    job_titles = get_distinct_values(Work, 'job_title', department, department_field='department')

    # Get distinct type_wagons for filtering dropdown
    type_wagons = get_type_wagon_filter_values(department, source_model='work')

    # Ensure consistent ordering for pagination
    works = works.order_by('work_name')

    # Paginate the results, 10 records per page
    page_obj = paginate_queryset(request, works)

    # Render the template with all context data
    return render(
        request,
        'work/work_list.html',
        {
            'works': page_obj,
            'page_obj': page_obj,
            'job_titles': job_titles,
            'type_wagons': type_wagons,
            'selected_department': department,
            'ALLOWED_WAGON_DEPARTMENTS': ALLOWED_WAGON_DEPARTMENTS, # Pass allowed departments to template
        }
    )
