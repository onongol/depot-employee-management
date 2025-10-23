from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .mixins import GenericContextMixin
from employee.models import Employee, Work, DailySalary, DailyWork, Piecework


class EmployeeContextMixin(GenericContextMixin):
    model = Employee
    object_type = _('Employee')
    success_url = reverse_lazy('employee_list')
    cancel_url = reverse_lazy('employee_list')
    object_name_func = staticmethod(lambda obj: f"{_('ID')}: {obj.employee_id}, {_('Name')}: {obj.name}")


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
        lambda obj: f"{_('ID')}: {obj.employee.employee_id}, {_('Name')}: {obj.employee.name}, {_('Date')}: {obj.salary_date}"
    )


class DailyWorkContextMixin(GenericContextMixin):
    model = DailyWork
    object_type = _('Daily Work')
    success_url = reverse_lazy('daily_work_list')
    cancel_url = reverse_lazy('daily_work_list')
    object_name_func = staticmethod(
        lambda obj: f"{_('Work')}: {obj.work.work_name}, { _('Type Work')}: {obj.type_work}, { _('Work Date')}: {obj.work_date}"
    )


class PieceworkContextMixin(GenericContextMixin):
    model = Piecework
    object_type = _('Piecework')
    success_url = reverse_lazy('piecework_list')
    cancel_url = reverse_lazy('piecework_list')
    object_name_func = staticmethod(
        lambda obj: (
            f"{obj.employee.employee_id}/{obj.employee.name} "
            f"{_('Work')}: {obj.work.work_name}, { _('Type Work')}: {obj.type_work}, { _('Work Date')}: {obj.work_date}"
        )
    )
