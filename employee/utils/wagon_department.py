from employee.constants.constants import ALLOWED_WAGON_DEPARTMENTS


def is_wagon_department(department):
    return department in ALLOWED_WAGON_DEPARTMENTS
