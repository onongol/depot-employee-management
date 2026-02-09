from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from employee.constants.constants import (
    DEPARTMENT_CHOICES,
    JOB_TITLE_CHOICES,
    RANK_CHOICES,
)
from employee.services.employee_salary_single import (
    get_employee_total_piecework_amount,
    get_employee_total_salary,
    get_employee_total_salary_day,
)


class Employee(models.Model):
    """This model represents an employee in the system."""

    employee_id = models.IntegerField(
        primary_key=True,
        null=False,
        validators=[MinValueValidator(1)],
        unique=True,
        error_messages={"unique": _("Must be unique.")},
    )
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=255, choices=DEPARTMENT_CHOICES)
    job_title = models.CharField(
        max_length=255, blank=False, null=False, choices=JOB_TITLE_CHOICES
    )
    rank = models.IntegerField(default=3, null=False, choices=RANK_CHOICES)
    money_per_hour = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        null=False,
        editable=True,
    )

    # Active status of the employee
    is_active = models.BooleanField(default=True)

    # Connection to the User model
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee_profile",
    )

    def __str__(self):
        return f"(ID: {self.employee_id}) {self.name}"

    # Domain/business helpers
    def get_total_salary_day(self, month, year):
        return get_employee_total_salary_day(self, month, year)

    def get_total_piecework_amount(self, month, year):
        return get_employee_total_piecework_amount(self, month, year)

    def get_total_salary(self, month, year):
        return get_employee_total_salary(self, month, year)
