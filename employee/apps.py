from django.apps import AppConfig


class EmployeeConfig(AppConfig):
    """AppConfig for the employee application."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employee'
