from django.contrib.auth.mixins import UserPassesTestMixin

from employee.constants.constants import GroupNames


class OnlyGroupMixin(UserPassesTestMixin):
    """Mixin to restrict access to users in specific groups or superusers."""
    group_names = []

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name__in=self.group_names).exists()


class OnlyAdminMixin(OnlyGroupMixin):
    """Mixin to restrict access to users in Payrolls group or superusers."""
    group_names = [GroupNames.PAYROLLS.value]


class OnlyCreaterMixin(OnlyGroupMixin):
    """Mixin to restrict access to users in Payrolls or Masters groups or superusers."""
    group_names = [GroupNames.PAYROLLS.value, GroupNames.MASTERS.value]
