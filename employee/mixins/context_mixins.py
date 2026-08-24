from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from employee.mixins.generic_mixins import GenericContextMixin
from employee.models import DailySalary, DailyWork, Employee, Piecework, Work


class ListUrlContextMixin(GenericContextMixin):
    """Base mixin to derive both success/cancel URLs from one route name."""

    list_url_name = None

    @property
    def success_url(self):
        return reverse_lazy(self.list_url_name)

    @property
    def cancel_url(self):
        return reverse_lazy(self.list_url_name)


class EmployeeContextMixin(ListUrlContextMixin):
    model = Employee
    object_type = _("Employee")
    list_url_name = "employee_list"


class WorkContextMixin(ListUrlContextMixin):
    model = Work
    object_type = _("Work")
    list_url_name = "work_list"


class DailySalaryContextMixin(ListUrlContextMixin):
    model = DailySalary
    object_type = _("Daily Salary")
    list_url_name = "daily_salary_list"


class DailyWorkContextMixin(ListUrlContextMixin):
    model = DailyWork
    object_type = _("Daily Work")
    list_url_name = "daily_work_list"


class PieceworkContextMixin(ListUrlContextMixin):
    model = Piecework
    object_type = _("Piecework")
    list_url_name = "piecework_list"
