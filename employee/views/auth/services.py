from django.contrib.auth.models import Group

from employee.constants.constants import GroupNames
from employee.models import Employee, Master, Payroll


def link_user_to_instance(user, instance, group_name):
    """Link user to the given instance and assign the appropriate group."""
    group, _ = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)
    instance.user = user
    instance.save()


def find_instance_by_id(register_id):
    """Find the instance and corresponding group by the given register ID."""
    for model, id_field, group_name in [
        (Employee, "employee_id", GroupNames.EMPLOYEES.value),
        (Master, "master_id", GroupNames.MASTERS.value),
        (Payroll, "payroll_id", GroupNames.PAYROLLS.value),
    ]:
        # Find the instance by ID
        instance = model.objects.filter(**{id_field: register_id}).first()
        if instance:
            return instance, group_name
    return None, None
