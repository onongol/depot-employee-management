from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from employee.models import Employee, Master, Payroll, Work

admin.site.unregister(User)
admin.site.unregister(Group)


class ImportExportMixin:
    import_form_class = ImportForm
    export_form_class = ExportForm


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin, ImportExportModelAdmin, ImportExportMixin):
    """Custom User Admin for the Employee Management System."""

    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    fieldsets = BaseUserAdmin.fieldsets
    add_fieldsets = BaseUserAdmin.add_fieldsets


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin, ImportExportModelAdmin):
    """Custom Group Admin for the Employee Management System."""

    pass


@admin.register(Employee)
class EmployeeAdmin(ModelAdmin, ImportExportModelAdmin, ImportExportMixin):
    list_display = (
        "employee_id",
        "name",
        "department",
        "job_title",
        "rank",
        "money_per_hour",
        "is_active",
    )
    search_fields = ("employee_id", "name")
    list_filter = ["department"]


@admin.register(Master)
class MasterAdmin(ModelAdmin, ImportExportModelAdmin, ImportExportMixin):
    list_display = ("master_id", "name")
    search_fields = ("master_id", "name")


@admin.register(Payroll)
class PayrollAdmin(ModelAdmin, ImportExportModelAdmin, ImportExportMixin):
    list_display = ("payroll_id", "name")
    search_fields = ("payroll_id", "name")


@admin.register(Work)
class WorkAdmin(ModelAdmin, ImportExportModelAdmin, ImportExportMixin):
    list_display = (
        "work_id",
        "department",
        "work_name",
        "type_material",
        "usage_material",
        "standard_time",
        "price",
    )
    search_fields = ("work_name", "type_material")
    list_filter = ["department"]
