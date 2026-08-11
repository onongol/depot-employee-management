from django.apps import AppConfig


class EmployeeConfig(AppConfig):
    """AppConfig for the employee application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "employee"
    verbose_name = "Operations"

    def ready(self):
        from allauth.account.signals import email_confirmed

        from employee.views.auth.services import link_confirmed_email_to_instance

        email_confirmed.connect(link_confirmed_email_to_instance)
