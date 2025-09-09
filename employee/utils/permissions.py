from django.contrib.auth.mixins import UserPassesTestMixin


class OnlyGroupMixin(UserPassesTestMixin):
    """Mixin to restrict access to users in specific groups or superusers."""
    group_names = []

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name__in=self.group_names).exists()


def is_admin(user):
    return user.is_superuser or user.groups.filter(name__in=['Payrolls']).exists()


class OnlyAdminMixin(OnlyGroupMixin):
    group_names = ['Payrolls']


def is_creater(user):
    return user.is_superuser or user.groups.filter(name__in=['Payrolls', 'Masters']).exists()


class OnlyCreaterMixin(OnlyGroupMixin):
    group_names = ['Payrolls', 'Masters']
