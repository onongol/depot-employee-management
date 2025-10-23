import json
from uuid import uuid4
from decimal import Decimal
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from employee.models import Employee
from employee.models import Piecework
from employee.models import Work
from employee.models import DailySalary
from employee.forms import PieceworkForm
from employee.utils.select_department import get_selected_department, expand_department
from employee.utils.selects import get_distinct_values
from employee.utils.select_type_wagon import get_type_wagon_filter_values
from employee.views.piecework.piecework_calculation import piecework_calculate_records
from employee.constants.constants import DEFAULT_WAGON_NUMBER, ALLOWED_WAGON_DEPARTMENTS


def daily_work_piecework_create(request):
    """View to create DailyWork and Piecework records together."""
    department = get_selected_department(request)
    # Filter employees and works by selected department, or show none if not selected
    employees = (
        Employee.objects.filter(department=department, is_active=True).order_by('employee_id')
        if department else Employee.objects.none()
    )
    # Expand department to include all related departments for works filtering
    departments = expand_department(department)
    works = (
        Work.objects.filter(department__in=departments).order_by('work_name')
        if departments else Work.objects.none()
    )

    # Get distinct job titles for filtering dropdown
    emp_job_titles = get_distinct_values(Employee, 'job_title', department, department_field='department')
    work_job_titles = get_distinct_values(
        Work, 'job_title', extra_filters={'department__in': departments} if departments else None
    )
    # Combine and sort job titles from both employees and works
    job_titles = sorted(set(list(emp_job_titles) + list(work_job_titles)))
    
    # Get distinct type_wagon for filtering dropdown if department allows wagons
    type_wagons = get_type_wagon_filter_values(department)

    today = timezone.now().date()
    errors = []

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

        # --- Create DailyWork record ---

        # Store created DailyWork records for linking to Piecework
        daily_works = {}

        # For each selected work, create a DailyWork record
        for wid in selected_work_ids:
            work_obj = Work.objects.get(pk=wid)
            amount_str = amounts.get(wid)
            amount = Decimal(amount_str) if amount_str else Decimal('0.00')

            # Create a DailyWork entry (one for each job for the day)
            from employee.models.daily_work_models import DailyWork # Import here to avoid circular imports

            # Create DailyWork record
            daily_work = DailyWork.objects.create(
                job_title=job_title or work_obj.job_title,
                work=work_obj,
                type_work=type_work,
                wagon_number=wagon_number,
                type_wagon=getattr(work_obj, 'type_wagon', None),
                amount=amount,
                work_date=work_date,
            )

            # Store for linking later
            daily_works[wid] = daily_work

        # --- Create Piecework ---
        
        # Validate required fields
        if not selected_employee_ids:
            errors.append(_("Please select at least one employee."))
        if not selected_work_ids:
            errors.append(_("Please select at least one work."))

        # Prefetch all selected works in a single query for efficient access
        works_dict = {str(work.pk): work for work in Work.objects.filter(pk__in=selected_work_ids)}

        # Check for missing amounts for any selected work
        missing_amounts = [
            wid for wid in selected_work_ids if not amounts.get(wid)
        ]    

        if not work_date or not type_work:
            errors.append(_("Please select work date, type work."))    
        elif missing_amounts:
            # If there are missing amounts, get the work names for error reporting
            missing_work_names = [
                works_dict[wid].work_name for wid in missing_amounts if wid in works_dict
            ]
            errors.append(
                _("Please fill in the amount for all selected work(s): %(works)s.") % {
                    'works': ', '.join(missing_work_names)
                }
            )
        else:
            # --- NEW DAILY SALARY CHECK LOGIC ---
            # Get all DailySalary records for selected employees and date
            employees_salary = DailySalary.objects.filter(
                employee__employee_id__in=selected_employee_ids,
                salary_date=work_date,
            )
            # Find employees without a DailySalary for the date
            employees_with_salary_ids = set(str(ds.employee.employee_id) for ds in employees_salary)
            missing_salary_employees = [
                emp for emp in Employee.objects.filter(employee_id__in=selected_employee_ids)
                if str(emp.employee_id) not in employees_with_salary_ids
            ]
            if missing_salary_employees:
                missing_names = [f"{emp.employee_id}/{emp.name}" for emp in missing_salary_employees]
                errors.append(
                    _("First create Daily Salary for these employee(s): %(employees)s for the selected date %(date)s.") % {
                        'employees': ', '.join(missing_names),
                        'date': work_date
                    }
                )
            else:
                # --- Business logic: Calculate amount_price for each employee and work ---
                # This function returns a list of dicts with calculated data and a list of errors                
                results, calc_errors = piecework_calculate_records(
                    employees_salary=employees_salary,
                    selected_work_ids=selected_work_ids,
                    amounts=amounts,
                    works_dict=works_dict,
                    work_date=work_date,
                    type_work=type_work,
                    wagon_number=wagon_number,
                )
                errors.extend(calc_errors)
                if not errors:
                    try:
                        # If something goes wrong (e.g., error creating Piecework), all changes will be rolled back (neither DailyWork nor Piecework will be saved)
                        with transaction.atomic():
                            group_id = str(uuid4())  # One group_id for the entire group
                            for data in results:
                                work_id = data['work_id']   # Extract work_id from data
                                data['daily_work'] = daily_works.get(work_id)  # Key point! Here we link Piecework with DailyWork.
                                data['group_id'] = group_id # Add group_id to data so that all Piecework in the group have the same ID.
                                Piecework.objects.create(**data)
                    except Exception as e:
                        errors.append(_("Error creating piecework records: %(error)s") % {'error': str(e)})
            if not errors:
                return redirect(f"{reverse('daily_work_list')}?department={department}")
                
    # Get existing pieceworks for the department for use in the frontend (e.g., to prevent duplicates)
    existing_pieceworks = list(
        Piecework.objects.filter(employee__department=department)
        .values(
            'employee_id', 'work_id', 'type_work', 'work_date', 'wagon_number'
        )
    )

    # Render the template with all context data
    return render(
        request,
        'daily_work/daily_work_piecework_create.html',
        {   
            'form': PieceworkForm(department=department),
            'object_type': 'Daily Work & Piecework',
            'employees': employees,
            'works': works,
            'today': today,
            'errors': errors,
            'selected_department': department,
            #'cancel_url': reverse('piecework_list'),
            'cancel_url': reverse('daily_work_list'),
            'existing_pieceworks_json': json.dumps(existing_pieceworks, cls=DjangoJSONEncoder), # Serialize existing pieceworks for frontend validation
            'job_titles': job_titles,
            'ALLOWED_WAGON_DEPARTMENTS': ALLOWED_WAGON_DEPARTMENTS,
            'type_wagons': type_wagons,
        }
    )
