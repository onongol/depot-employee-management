from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from simple_history.models import HistoricalRecords

from employee.models.models_mixins.soft_delete_mixin import SoftDeleteMixin
from employee.services.soft_delete_manager import SoftDeleteManager


class Payroll(SoftDeleteMixin, models.Model):
    """This model represents a payroll specialist in the system."""

    payroll_id = models.IntegerField(
        primary_key=True, null=False, validators=[MinValueValidator(1)], unique=True
    )
    name = models.CharField(max_length=255)

    # Active status of the employee
    is_active = models.BooleanField(default=True)

    # Soft delete flag: True if the record is considered deleted, False otherwise.
    is_deleted = models.BooleanField(default=False, db_index=True)

    # Connection to the User model
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payroll_profile",
    )

    history = HistoricalRecords()

    # Custom managers to handle soft deletion logic.
    objects = SoftDeleteManager()
    all_objects = SoftDeleteManager(only_alive=False)

    def __str__(self):
        return f"(ID: {self.payroll_id}) {self.name}"
