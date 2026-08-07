from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from employee.models.models_mixins.soft_delete_mixin import SoftDeleteMixin
from employee.services.soft_delete_manager import SoftDeleteManager


class Payroll(SoftDeleteMixin, models.Model):
    """This model represents a payroll specialist in the system."""

    id = models.AutoField(primary_key=True)

    payroll_id = models.IntegerField(
        null=False,
        validators=[MinValueValidator(1)],
    )
    payroll_name = models.CharField(max_length=255, db_index=True)

    # Email on file for this payroll specialist, used to verify self-registration.
    email = models.EmailField(
        null=True,
        blank=True,
        unique=True,
    )

    # Active status of the employee
    is_active = models.BooleanField(default=True)

    # Soft delete flag: True if the record is considered deleted, False otherwise.
    is_deleted = models.BooleanField(default=False, db_index=True)

    # Connection to the User model
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
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
        return f"(ID: {self.payroll_id}) {self.payroll_name}"

    def clean(self):
        """
        Ensure payroll_id is unique among non-deleted records (soft delete aware, for MySQL).
        """
        if not self.is_deleted:
            qs = Payroll.objects.filter(
                payroll_id=self.payroll_id,
                is_deleted=False,
            )
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError(
                    {
                        "payroll_id": _("Must be unique."),
                    }
                )
