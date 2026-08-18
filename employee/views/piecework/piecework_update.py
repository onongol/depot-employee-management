from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from employee.forms import UpdatePieceworkForm
from employee.mixins.context_mixins import PieceworkContextMixin
from employee.models import DailySalary
from employee.services.calculate_piecework_update import calculate_piecework_update
from employee.utils.select_department import get_selected_department


class PieceworkUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, PieceworkContextMixin, UpdateView
):
    permission_required = "employee.change_piecework"
    form_class = UpdatePieceworkForm
    template_name = "piecework/piecework_update.html"
    success_url = reverse_lazy("piecework_list")

    def get_form_kwargs(self):
        """Add department to form kwargs for filtering."""
        kwargs = super().get_form_kwargs()
        kwargs["department"] = get_selected_department(self.request)
        return kwargs

    def form_valid(self, form):
        """Handle form validation and calculate amount price based on daily salary."""
        piecework = form.instance
        employee = piecework.employee
        work = piecework.work
        work_date = piecework.work_date
        amount = form.cleaned_data.get("amount")

        wagon_number = form.cleaned_data.get("wagon_number")
        if not wagon_number:
            piecework.wagon_number = None

        if not piecework.daily_work_id:
            form.add_error(None, _("Piecework must be linked to Daily Work."))
            return self.form_invalid(form)

        daily_salary = DailySalary.objects.filter(
            employee=employee, salary_date=work_date
        ).first()

        # Get all employee IDs from pieceworks linked to the same DailyWork for accurate calculation
        employee_ids = piecework.daily_work.pieceworks.values_list(
            "employee_id", flat=True
        )

        # Get all DailySalary records for employees in the same department and date for accurate calculation
        employees_salary = DailySalary.objects.filter(
            employee__department=piecework.daily_work.department,
            employee_id__in=employee_ids,
            salary_date=work_date,
        )

        amount_price = calculate_piecework_update(
            work, amount, daily_salary, employees_salary
        )

        # Save the updated piecework with the new amount price
        obj = form.save(commit=False)
        obj.amount_price = amount_price
        obj.save()

        return super().form_valid(form)
