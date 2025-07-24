from django.contrib import admin

# Register your models here.
from .models.employee_models import Employee
from .models.master_models import Master


admin.site.register(Employee)

admin.site.register(Master)