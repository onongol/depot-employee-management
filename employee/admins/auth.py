from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.paginator import InfinitePaginator

from employee.admins.common import ImportExportMixin

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin, ImportExportModelAdmin, ImportExportMixin):
    """Custom User Admin for the Employee Management System."""

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
