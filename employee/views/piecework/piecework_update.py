from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from employee.forms import UpdatePieceworkForm
from employee.mixins.context_mixins import PieceworkContextMixin
from employee.mixins.permissions_mixins import OnlyPayrollsMixin
from employee.models import DailySalary
from employee.services.calculate_piecework_update import calculate_piecework_update
from employee.utils.select_department import get_selected_department


class PieceworkUpdateView(
    LoginRequiredMixin, OnlyPayrollsMixin, PieceworkContextMixin, UpdateView
):
    login_url = "login"
    form_class = UpdatePieceworkForm
    template_name = "piecework/piecework_update.html"

    def get_form_kwargs(self):
        """Add department to form kwargs for filtering."""
        kwargs = super().get_form_kwargs()
        kwargs["department"] = get_selected_department(self.request)
        return kwargs

    def form_valid(self, form):
        """Handle form validation and calculate amount price based on daily salary."""
        piecework = form.instance
        amount = form.cleaned_data.get("amount")
        work = piecework.work
        work_date = piecework.work_date
        employee = piecework.employee

        wagon_number = form.cleaned_data.get("wagon_number")
        if not wagon_number:
            piecework.wagon_number = None

        # Get the daily salary for the employee on the work date
        daily_salary = DailySalary.objects.filter(
            employee=employee, salary_date=work_date
        ).first()

        if not piecework.daily_work_id:
            form.add_error(None, _("Piecework must be linked to DailyWork."))
            return self.form_invalid(form)

        # Use the same salary pool as piecework creation/sync: only employees linked
        # to the same DailyWork should affect price distribution.
        employee_ids = piecework.daily_work.pieceworks.values_list(
            "employee_id", flat=True
        )
        employees_salary = DailySalary.objects.filter(
            employee__department=piecework.daily_work.department,
            employee_id__in=employee_ids,
            salary_date=work_date,
        )

        # Calculate amount_price using business logic function
        amount_price = calculate_piecework_update(
            work, amount, daily_salary, employees_salary
        )

        piecework.amount_price = amount_price

        form.save()

        return redirect("piecework_list")
