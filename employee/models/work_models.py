from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from employee.constants.constants import (
    ALLOWED_WAGON_DEPARTMENTS,
    JOB_TITLE_CHOICES,
    TYPE_WAGON_CHOICES,
)
from employee.models.models_mixins.display_mixins import (
    TypeMaterialDisplayMixin,
    TypeWagonDisplayMixin,
)
from employee.models.models_mixins.soft_delete_mixin import SoftDeleteMixin
from employee.services.soft_delete_manager import SoftDeleteManager


class Work(
    SoftDeleteMixin, TypeMaterialDisplayMixin, TypeWagonDisplayMixin, models.Model
):
    """This model represents a work item in the system."""

    id = models.AutoField(primary_key=True)

    work_name = models.CharField(max_length=255, blank=False, null=False, db_index=True)
    department = models.CharField(
        max_length=255, blank=False, null=False, db_index=True
    )
    job_title = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        choices=JOB_TITLE_CHOICES,
        db_index=True,
    )
    type_wagon = models.CharField(
        max_length=100,
        choices=TYPE_WAGON_CHOICES,
        blank=True,
        null=True,
        db_index=True,
    )
    type_material = models.CharField(max_length=255, blank=True, null=True)
    usage_material = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        default=Decimal("0.0000"),
        validators=[MinValueValidator(0)],
        blank=True,
        null=False,
    )
    standard_time = models.DecimalField(
        max_digits=20,
        decimal_places=6,
        validators=[MinValueValidator(0.000001)],
    )
    price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )

    # Soft delete flag: True if the record is considered deleted, False otherwise.
    is_deleted = models.BooleanField(default=False, db_index=True)

    # Historical records for auditing changes to instances over time.
    history = HistoricalRecords()

    # Custom managers to handle soft deletion logic.
    objects = SoftDeleteManager()
    all_objects = SoftDeleteManager(only_alive=False)

    class Meta:
        """
        Model-level metadata:
        - Enforces business rules via database constraints:
        * type_wagon can only be set for allowed departments; otherwise it must be NULL.
        * work_name must be unique within the same department.
        """

        constraints = [
            # Ensure type_wagon is only set for allowed departments
            models.CheckConstraint(
                name="type_wagon_only_for_allowed_departments",
                check=Q(department__in=ALLOWED_WAGON_DEPARTMENTS)
                | Q(type_wagon__isnull=True),
            ),
            # Ensure work_name is unique within the same department, only for
            models.UniqueConstraint(
                fields=["department", "work_name"],
                condition=Q(is_deleted=False),
                name="unique_work_name_per_department",
            ),
        ]

    def __str__(self):
        return self.work_name

    def save(self, *args, **kwargs):
        """
        Ensure the instance is valid and normalized before persisting:
        - Call full_clean() to run model/field validators and clean().
        - Then save to the database.
        """
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        """
        Normalize and validate fields before saving:
        - If type_material is empty, set it to None and reset usage_material to 0.
        - Enforce business rule for type_wagon:
          only allowed for departments in ALLOWED_WAGON_DEPARTMENTS, else set to None.
        """
        if not self.type_material:
            self.type_material = None
            self.usage_material = Decimal("0.0000")

        if self.department not in ALLOWED_WAGON_DEPARTMENTS:
            self.type_wagon = None
        elif not self.type_wagon:
            self.type_wagon = None

        # Soft-delete aware uniqueness check for MySQL
        if not self.is_deleted:
            qs = Work.objects.filter(
                department=self.department,
                work_name=self.work_name,
                is_deleted=False,
            )
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError({"work_name": _("Must be unique.")})

    def get_update_url(self):
        """Get the URL for updating this work instance."""
        return reverse("work_update", args=[self.pk])

    def get_dom_attrs(self):
        """Get the DOM attributes for this work instance."""
        return {
            "data-work-name": self.work_name,
            "data-row-id": self.pk,
            "data-row-name": str(self),
            "data-edit-url": self.get_update_url(),
        }
