from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _

from employee.mixins.context_mixins import WorkContextMixin
from employee.mixins.delete_mixins import DeleteProtectionMixin
from employee.mixins.block_message_mixins import BlockMessageMixin
from employee.models import Work 
from employee.models import Piecework
from employee.forms import WorkForm, UpdateWorkForm
from employee.utils.select_department import get_selected_department
from employee.utils.filters import filter_works
from employee.utils.pagination import paginate_queryset
from employee.utils.permissions import OnlyAdminMixin
from employee.utils.selects import get_distinct_values
from employee.utils.select_type_wagon import get_type_wagon_filter_values
from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS


class WorkCreateView(LoginRequiredMixin, OnlyAdminMixin, WorkContextMixin, SuccessMessageMixin, CreateView):
    login_url = 'login'
    form_class = WorkForm
    template_name = "work/work_create.html" 
    success_message = _("Work %(work_name)s created successfully.")

    def get_form_kwargs(self):
        """Set initial department based on user selection."""
        kwargs = super().get_form_kwargs()
        kwargs['department'] = get_selected_department(self.request)
        return kwargs
    
    def get_context_data(self, **kwargs):
        """Add context to show/hide type_wagon field based on department."""
        ctx = super().get_context_data(**kwargs)
        dept = get_selected_department(self.request)
        ctx['SHOW_TYPE_WAGON'] = dept in ALLOWED_WAGON_DEPARTMENTS
        return ctx


class WorkUpdateView(LoginRequiredMixin, OnlyAdminMixin, WorkContextMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    form_class = UpdateWorkForm
    template_name = "work/work_update.html"
    success_message = _("Work updated successfully.")

    def get_form_kwargs(self):
        """Set initial department based on user selection."""
        kwargs = super().get_form_kwargs()
        kwargs['department'] = get_selected_department(self.request)
        return kwargs
    
    def get_context_data(self, **kwargs):
        """Add context to show/hide type_wagon field based on department."""
        ctx = super().get_context_data(**kwargs)
        dept = getattr(self.object, 'department', None) or get_selected_department(self.request)
        ctx['SHOW_TYPE_WAGON'] = dept in ALLOWED_WAGON_DEPARTMENTS
        return ctx


class WorkDeleteView(LoginRequiredMixin, OnlyAdminMixin, WorkContextMixin, BlockMessageMixin, DeleteProtectionMixin, DeleteView):
    login_url = 'login'
    template_name = "work/work_confirm_delete.html"
    block_related_models = [_('Daily Work'), _('Piecework')]

    # Get related piecework records to check if deletion is allowed.
    def get_related_objects(self):
        return Piecework.objects.filter(work=self.object)
    
    # Handle the deletion and send a warning.
    def get_redirect_url(self):
        return self.success_url
    
    def get_object_name(self):
        return f"{self.object.work_name}"


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
