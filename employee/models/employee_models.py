from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from employee.constants.constants import (
    DEPARTMENT_CHOICES,
    JOB_TITLE_CHOICES,
    RANK_CHOICES,
)
from employee.models.models_mixins.soft_delete_mixin import SoftDeleteMixin
from employee.services.employee_salary_single import (
    get_employee_total_piecework_amount,
    get_employee_total_salary,
    get_employee_total_salary_day,
)
from employee.services.soft_delete_manager import SoftDeleteManager


class Employee(SoftDeleteMixin, models.Model):
    """This model represents an employee in the system."""

    id = models.AutoField(primary_key=True)

    employee_id = models.IntegerField(
        null=False,
        validators=[MinValueValidator(1)],
    )
    employee_name = models.CharField(max_length=255, db_index=True)
    department = models.CharField(
        max_length=255, choices=DEPARTMENT_CHOICES, db_index=True
    )
    job_title = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        choices=JOB_TITLE_CHOICES,
        db_index=True,
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

    # Soft delete flag: True if the record is considered deleted, False otherwise.
    is_deleted = models.BooleanField(default=False)

    # Connection to the User model
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee_profile",
    )

    # Historical records for tracking changes.
    history = HistoricalRecords()

    # Custom managers to handle soft deletion logic.
    objects = SoftDeleteManager()
    all_objects = SoftDeleteManager(only_alive=False)

    # Meta options for database indexing and string representation.
    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "is_deleted",
                    "is_active",
                    "department",
                    "job_title",
                    "employee_id",
                ]
            ),
            models.Index(fields=["employee_id", "is_deleted"]),
        ]

    def __str__(self):
        return f"(ID: {self.employee_id}) {self.employee_name}"

    def clean(self):
        """
        Ensure employee_id is unique among non-deleted records (soft delete aware, for MySQL).
        """
        if not self.is_deleted:
            qs = Employee.objects.filter(
                employee_id=self.employee_id,
                is_deleted=False,
            )
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError(
                    {
                        "employee_id": _("Must be unique."),
                    }
                )

    def get_update_url(self):
        return reverse("employee_update", args=[self.pk])

    def get_activate_url(self):
        return reverse("employee_activate", args=[self.pk])

    def get_deactivate_url(self):
        return reverse("employee_deactivate", args=[self.pk])

    def get_dom_attrs(self):
        return {
            "data-emp-id": self.employee_id,
            "data-emp-name": self.employee_name,
            "data-row-id": self.pk,
            "data-row-name": str(self),
            "data-edit-url": self.get_update_url(),
            "data-is-active": "True" if self.is_active else "False",
            "data-activate-url": self.get_activate_url()
            if hasattr(self, "get_activate_url")
            else "",
            "data-deactivate-url": self.get_deactivate_url()
            if hasattr(self, "get_deactivate_url")
            else "",
        }

    # Domain/business helpers
    def get_total_salary_day(self, month, year):
        return get_employee_total_salary_day(self, month, year)

    def get_total_piecework_amount(self, month, year):
        return get_employee_total_piecework_amount(self, month, year)

    def get_total_salary(self, month, year):
        return get_employee_total_salary(self, month, year)
