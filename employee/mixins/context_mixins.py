from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from employee.mixins.generic_mixins import GenericContextMixin
from employee.models import DailySalary, DailyWork, Employee, Piecework, Work


class EmployeeContextMixin(GenericContextMixin):
    model = Employee
    object_type = _("Employee")
    success_url = reverse_lazy("employee_list")
    cancel_url = reverse_lazy("employee_list")


class WorkContextMixin(GenericContextMixin):
    model = Work
    object_type = _("Work")
    success_url = reverse_lazy("work_list")
    cancel_url = reverse_lazy("work_list")


class DailySalaryContextMixin(GenericContextMixin):
    model = DailySalary
    object_type = _("Daily Salary")
    success_url = reverse_lazy("daily_salary_list")
    cancel_url = reverse_lazy("daily_salary_list")


class DailyWorkContextMixin(GenericContextMixin):
    model = DailyWork
    object_type = _("Daily Work")
    success_url = reverse_lazy("daily_work_list")
    cancel_url = reverse_lazy("daily_work_list")


class PieceworkContextMixin(GenericContextMixin):
    model = Piecework
    object_type = _("Piecework")
    success_url = reverse_lazy("piecework_list")
    cancel_url = reverse_lazy("piecework_list")
