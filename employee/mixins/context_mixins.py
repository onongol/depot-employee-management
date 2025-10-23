from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .mixins import GenericContextMixin
from employee.models import Employee, Work, DailySalary, DailyWork, Piecework


class EmployeeContextMixin(GenericContextMixin):
    model = Employee
    object_type = _('Employee')
    success_url = reverse_lazy('employee_list')
    cancel_url = reverse_lazy('employee_list')
    object_name_func = staticmethod(lambda obj: f"{obj.employee_id}/{obj.name}")


class WorkContextMixin(GenericContextMixin):
    model = Work
    object_type = _('Work')
    success_url = reverse_lazy('work_list')
    cancel_url = reverse_lazy('work_list')
    object_name_func = staticmethod(lambda obj: str(obj))


class DailySalaryContextMixin(GenericContextMixin):
    model = DailySalary
    object_type = _('Daily Salary')
    success_url = reverse_lazy('daily_salary_list')
    cancel_url = reverse_lazy('daily_salary_list')
    object_name_func = staticmethod(
        lambda obj: f"{obj.employee.employee_id}/{obj.employee.name}/{obj.salary_date}"
    )


class DailyWorkContextMixin(GenericContextMixin):
    model = DailyWork
    object_type = _('Daily Work')
    success_url = reverse_lazy('daily_work_list')
    cancel_url = reverse_lazy('daily_work_list')
    object_name_func = staticmethod(
        lambda obj: f"{obj.work.work_name}/{obj.type_work}/{obj.work_date}"
    )


class PieceworkContextMixin(GenericContextMixin):
    model = Piecework
    object_type = _('Piecework')
    success_url = reverse_lazy('piecework_list')
    cancel_url = reverse_lazy('piecework_list')
    object_name_func = staticmethod(
        lambda obj: (
            f"{obj.employee.employee_id}/{obj.employee.name} "
            f"{obj.work.work_name}/{obj.type_work}/{obj.work_date}"
        )
    )
