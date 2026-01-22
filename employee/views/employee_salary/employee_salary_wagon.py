from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS, GROUP_WAGON


def is_wagon_group(*, department: str | None, group: str | None) -> bool:
    """Checks if wagon grouping is active for department and request."""
    
    return (group == GROUP_WAGON) and (department in ALLOWED_WAGON_DEPARTMENTS)
