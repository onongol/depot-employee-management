from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from employee.constants.constants import DEFAULT_WAGON_NUMBER
from employee.mixins.success_messages_mixins import send_daily_work_piecework_created
from .context_builders import build_daily_piecework_context
from .daily_work_piecework_service import process_piecework


def daily_work_piecework_create(request):
    """Handle the creation of daily work and piecework entries."""
    # Build the context for the view
    context = build_daily_piecework_context(request)

    # Handle form submission
    if request.method == 'POST':
        work_date = request.POST.get('work_date')
        type_work = request.POST.get('type_work')
        wagon_number = request.POST.get('wagon_number', '').strip()
        if not wagon_number or wagon_number == DEFAULT_WAGON_NUMBER:
            wagon_number = None
        selected_employee_ids = request.POST.getlist('employee_ids')
        selected_work_ids = request.POST.getlist('work_ids')
        amounts = {wid: request.POST.get(f'amount_{wid}') for wid in selected_work_ids}
        job_title = request.POST.get('job_title')

        # Process piecework creation
        results, works_dict, errors = process_piecework({
            'work_date': work_date,
            'type_work': type_work,
            'wagon_number': wagon_number,
            'selected_employee_ids': selected_employee_ids,
            'selected_work_ids': selected_work_ids,
            'amounts': amounts,
            'job_title': job_title,
        })

        # If there are errors, re-render the form with error messages
        if errors:
            context['errors'] = errors
            return render(request, 'daily_work/daily_work_piecework_create.html', context)

        # On successful creation, redirect to the daily work list with a success message
        send_daily_work_piecework_created(request, results=results, works_dict=works_dict, work_date=work_date)

        # Redirect to the daily work list with the selected department as a query parameter
        department = context.get('selected_department')

        return redirect(f"{reverse('daily_work_list')}?department={department}")

    # Render the template with all context data
    return render(request, 'daily_work/daily_work_piecework_create.html', context)
