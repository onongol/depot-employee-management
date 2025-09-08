from django.urls import reverse_lazy

from .mixins import GenericContextMixin
from employee.models import Employee, Work, DailyPay, Piecework


class EmployeeContextMixin(GenericContextMixin):
    model = Employee
    object_type = 'Employee'
    success_url = reverse_lazy('employee_list')
    cancel_url = reverse_lazy('employee_list')
    object_name_func = staticmethod(lambda obj: f"{obj.employee_id}/{obj.name}")


class WorkContextMixin(GenericContextMixin):
    model = Work
    object_type = 'Work'
    success_url = reverse_lazy('work_list')
    cancel_url = reverse_lazy('work_list')
    object_name_func = staticmethod(lambda obj: str(obj))


class DailyPayContextMixin(GenericContextMixin):
    model = DailyPay
    object_type = 'Daily Pay'
    success_url = reverse_lazy('daily_pay_list')
    cancel_url = reverse_lazy('daily_pay_list')
    object_name_func = staticmethod(
        lambda obj: f"{obj.employee.employee_id}/{obj.employee.name} - {obj.salary_date}"
    )


class PieceworkContextMixin(GenericContextMixin):
    model = Piecework
    object_type = 'Piecework'
    success_url = reverse_lazy('piecework_list')
    cancel_url = reverse_lazy('piecework_list')
    object_name_func = staticmethod(
        lambda obj: (
            f"{obj.employee.employee_id}/{obj.employee.name} "
            f"Work: {obj.work.work_name}, Type Work: {obj.type_work}, Work Date:{obj.work_date}"
        )
    )
