from django.contrib.auth.mixins import UserPassesTestMixin

group_names = ['Payrolls']
group_names_1 = ['Payrolls', 'Masters']


def is_admin(user):
    return user.is_superuser or user.groups.filter(name__in=group_names).exists()


class OnlyAdminMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name__in=group_names).exists() 
    

def is_creater(user):
    return user.is_superuser or user.groups.filter(name__in=group_names_1).exists()


class OnlyCreaterMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name__in=group_names_1).exists()
