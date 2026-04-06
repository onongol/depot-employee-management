from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from import_export.admin import (
    ExportActionModelAdmin,
    ExportMixin,
    ImportExportModelAdmin,
)
from simple_history.admin import SimpleHistoryAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import (
    ChoicesDropdownFilter,
    FieldTextFilter,
    MultipleChoicesDropdownFilter,
)
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.paginator import InfinitePaginator

from employee.models import (
    DailySalary,
    DailyWork,
    Employee,
    Master,
    Payroll,
    Piecework,
    Work,
)

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

    paginator = InfinitePaginator
    show_full_result_count = True


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin, ImportExportModelAdmin):
    """Custom Group Admin for the Employee Management System."""

    pass


@admin.register(Master)
class MasterAdmin(
    ModelAdmin, SimpleHistoryAdmin, ImportExportModelAdmin, ImportExportMixin
):
    list_display = (
        "master_id",
        "name",
        "department",
        "is_active",
    )
    search_fields = (
        "master_id",
        "name",
    )
    search_help_text = "Search by master ID or name"
    list_filter = ["department", "is_active"]
    list_editable = ("is_active",)
    ordering = ("-master_id",)


@admin.register(Payroll)
class PayrollAdmin(
    ModelAdmin, SimpleHistoryAdmin, ImportExportModelAdmin, ImportExportMixin
):
    list_display = (
        "payroll_id",
        "name",
        "is_active",
    )
    search_fields = (
        "payroll_id",
        "name",
    )
    search_help_text = "Search by payroll ID or name"
    list_filter = ["is_active"]
    list_editable = ("is_active",)
    ordering = ("-payroll_id",)


@admin.register(Employee)
class EmployeeAdmin(
    ModelAdmin, SimpleHistoryAdmin, ImportExportModelAdmin, ImportExportMixin
):
    list_display = (
        "employee_id",
        "name",
        "department",
        "job_title",
        "rank",
        "money_per_hour",
        "is_active",
    )
    search_fields = (
        "employee_id",
        "name",
    )
    search_help_text = "Search by employee ID or name"
    list_filter_submit = True
    list_filter = ["department", ("job_title", ChoicesDropdownFilter), "is_active"]
    list_editable = ("is_active",)
    ordering = ("-employee_id",)


@admin.register(Work)
class WorkAdmin(
    ModelAdmin, SimpleHistoryAdmin, ImportExportModelAdmin, ImportExportMixin
):
    list_display = (
        "work_id",
        "department",
        "job_title",
        "work_name",
        "type_wagon",
        "type_material",
        "usage_material",
        "standard_time",
        "price",
    )
    search_fields = ("work_name",)
    search_help_text = "Search by work name"
    list_filter_submit = True
    list_filter = [
        "department",
        ("job_title", ChoicesDropdownFilter),
        ("type_wagon", MultipleChoicesDropdownFilter),
    ]
    readonly_fields = ("work_id",)
    ordering = ("-work_id",)


@admin.register(DailySalary)
class DailySalaryAdmin(
    ModelAdmin, SimpleHistoryAdmin, ExportActionModelAdmin, ExportMixin, ExportForm
):
    list_display = (
        "salary_id",
        "employee_id",
        "employee_name",
        "department",
        "employee__job_title",
        "hours_per_day",
        "salary_day",
        "salary_date",
        "record_date",
    )
    search_fields = (
        "employee__employee_id",
        "employee_name",
    )
    search_help_text = "Search by employee ID or name"
    list_filter_submit = True
    list_filter = [
        "department",
        ("employee__job_title", ChoicesDropdownFilter),
    ]
    date_hierarchy = "salary_date"
    ordering = ("-salary_date", "-record_date")
    list_display_links = ("salary_id", "employee__employee_id", "employee_name")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DailyWork)
class DailyWorkAdmin(
    ModelAdmin, SimpleHistoryAdmin, ExportActionModelAdmin, ExportMixin, ExportForm
):
    list_display = (
        "id",
        "work_name",
        "department",
        "job_title",
        "type_work",
        "wagon_number",
        "type_wagon",
        "amount",
        "amount_time",
        "amount_price",
        "amount_material",
        "work_date",
        "record_date",
    )
    search_fields = ("work_name",)
    search_help_text = "Search by work name"
    list_filter_submit = True
    list_filter = [
        "department",
        ("job_title", ChoicesDropdownFilter),
        ("wagon_number", FieldTextFilter),
        ("type_work", MultipleChoicesDropdownFilter),
        ("type_wagon", MultipleChoicesDropdownFilter),
    ]
    date_hierarchy = "work_date"
    ordering = ("-work_date", "-record_date")
    list_display_links = (
        "id",
        "work_name",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Piecework)
class PieceworkAdmin(ModelAdmin, ExportActionModelAdmin, ExportMixin, ExportForm):
    list_display = (
        "record_id",
        "employee_id",
        "employee_name",
        "department",
        "job_title",
        "work_name",
        "type_work",
        "wagon_number",
        "type_wagon",
        "amount",
        "amount_time",
        "amount_price",
        "amount_material",
        "work_date",
        "record_date",
    )
    search_fields = (
        "employee__employee_id",
        "employee_name",
    )
    search_help_text = "Search by employee ID or name"
    list_filter_submit = True
    list_filter = [
        "department",
        ("job_title", ChoicesDropdownFilter),
        ("work_name", FieldTextFilter),
        "type_work",
        ("wagon_number", FieldTextFilter),
        ("type_wagon", MultipleChoicesDropdownFilter),
    ]
    date_hierarchy = "work_date"
    ordering = ("-work_date", "-record_date")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
