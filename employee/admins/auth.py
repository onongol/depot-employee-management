from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import FieldTextFilter
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from employee.models import RegistrationRequest

User = get_user_model()

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass


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


@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(ModelAdmin):
    """Read-only view of pending and confirmed self-registrations."""

    list_display = (
        "user",
        "register_id",
        "group_name",
        "created_at",
        "confirmed_at",
    )
    search_fields = ("user__username", "user__email", "register_id__exact")
    list_filter = ("group_name",)
    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
