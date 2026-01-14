from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS, GROUP_WAGON


def is_wagon_group(*, department: str | None, group: str | None) -> bool:
    '''
    Centralized check for "wagon mode": enabled only when the request asks for wagon grouping
    (group == GROUP_WAGON) and the selected department supports wagons. This flag is reused by
    exports and calculations to (1) group salaries by wagon, (2) apply wagon_number filtering,
    and (3) show/hide the Wagon column consistently.
    '''
    return (group == GROUP_WAGON) and (department in ALLOWED_WAGON_DEPARTMENTS)
