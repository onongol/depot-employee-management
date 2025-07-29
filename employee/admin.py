from django.contrib import admin
from unfold.admin import ModelAdmin

from .models.employee_models import Employee
from .models.master_models import Master
from .models.payroll_models import Payroll

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    fieldsets = BaseUserAdmin.fieldsets
    add_fieldsets = BaseUserAdmin.add_fieldsets


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

@admin.register(Employee)
class EmployeeAdmin(ModelAdmin):
    list_display = ("employee_id", "name", "department")
    search_fields = ("employee_id", "name")

@admin.register(Master)
class MasterAdmin(ModelAdmin):
    list_display = ("master_id", "name")
    search_fields = ("master_id", "name")

@admin.register(Payroll)
class PayrollAdmin(ModelAdmin):
    list_display = ("payroll_id", "name")
    search_fields = ("payroll_id", "name")
