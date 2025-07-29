from django.contrib import admin

from .models.employee_models import Employee
from .models.master_models import Master
from .models.payroll_models import Payroll


admin.site.register(Employee)

admin.site.register(Master)

admin.site.register(Payroll)
