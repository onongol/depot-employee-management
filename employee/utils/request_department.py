from employee.constants.constants import DEPARTMENTS, EMPLOYEE_GROUP, MASTER_GROUP
from employee.models import Employee, Master
from employee.utils.user_roles import get_user_groups


def get_user_department(user):
    """Get the department of the user from Employee or Master models."""
    for model in (Employee, Master):
        try:
            obj = model.objects.get(user=user, is_active=True)
            if not obj:
                continue
            department = getattr(obj, "department", None)
            if department in DEPARTMENTS:
                return department
        except model.DoesNotExist:
            continue
    return None


def get_selected_department_from_request(request):
    """Get and cache the selected department on request; Employees/Masters are locked to their own."""
    if request.user.is_authenticated:
        groups = get_user_groups(request)
        if EMPLOYEE_GROUP in groups or MASTER_GROUP in groups:
            request.selected_department = get_user_department(request.user)
            return request.selected_department

    selected_department = request.GET.get("department") or request.session.get(
        "department"
    )
    if selected_department not in DEPARTMENTS:
        selected_department = None
    request.selected_department = selected_department
    return selected_department
