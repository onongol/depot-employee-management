from django.contrib import admin

# Register your models here.
from .models.employee_models import Employee

admin.site.register(Employee)