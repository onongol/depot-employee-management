import contextlib

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import FieldTextFilter
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

User = get_user_model()

with contextlib.suppress(admin.sites.NotRegistered):
    admin.site.unregister(User)

with contextlib.suppress(admin.sites.NotRegistered):
    admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
        "date_joined",
    )

    search_fields = ("username",)
    search_help_text = "Search by username"
    list_filter_submit = True

    list_filter = (
        ("email", FieldTextFilter),
        ("first_name", FieldTextFilter),
        ("last_name", FieldTextFilter),
        "is_active",
        "is_staff",
        "is_superuser",
        "groups",
    )

    ordering = (
        "-last_login",
        "-date_joined",
    )
    readonly_fields = ("last_login", "date_joined")

    def get_readonly_fields(self, request, obj=None):
        """username is auto-synced from email; read-only once the user exists so editing it here can't look like it worked."""
        readonly = super().get_readonly_fields(request, obj)
        if obj is not None:
            readonly = (*readonly, "username")
        return readonly

    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    fieldsets = BaseUserAdmin.fieldsets
    add_fieldsets = BaseUserAdmin.add_fieldsets


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    """Manage auth groups and their assigned permissions."""

    list_display = ("name",)
    search_fields = ("name",)
    search_help_text = "Search by group name"
    ordering = ("name",)
