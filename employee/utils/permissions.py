from django.contrib.auth.mixins import UserPassesTestMixin

from employee.constants.constants import GroupNames

class OnlyGroupMixin(UserPassesTestMixin):
    """Mixin to restrict access to users in specific groups or superusers."""
    group_names = []

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name__in=self.group_names).exists()


def is_admin(user):
    return user.is_superuser or user.groups.filter(name__in=[GroupNames.PAYROLLS.value]).exists()


class OnlyAdminMixin(OnlyGroupMixin):
    group_names = [GroupNames.PAYROLLS.value]


def is_creater(user):
    return user.is_superuser or user.groups.filter(name__in=[GroupNames.PAYROLLS.value, GroupNames.MASTERS.value]).exists()


class OnlyCreaterMixin(OnlyGroupMixin):
    group_names = [GroupNames.PAYROLLS.value, GroupNames.MASTERS.value]
