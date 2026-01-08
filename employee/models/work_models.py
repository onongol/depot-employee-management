from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q

from employee.constants.constants import (ALLOWED_WAGON_DEPARTMENTS,
                                          JOB_TITLE_CHOICES,
                                          TYPE_WAGON_CHOICES)
from employee.models.models_mixins.display_mixins import (TypeMaterialDisplayMixin,
                                                          TypeWagonDisplayMixin)


class Work(TypeMaterialDisplayMixin, TypeWagonDisplayMixin, models.Model):
    """This model represents a work item in the system."""
    work_id = models.AutoField(
        primary_key=True, 
        editable=False
    )
    department = models.CharField(
        max_length=255, 
        blank=False, 
        null=False
    )
    job_title = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        choices=JOB_TITLE_CHOICES
    )
    work_name = models.CharField(
        max_length=255
    )
    type_wagon = models.CharField(
        max_length=100,
        choices=TYPE_WAGON_CHOICES,
        blank=True,
        null=True,
    )
    type_material = models.CharField(
        max_length=255, 
        blank=True, 
        null=True
    )
    usage_material = models.DecimalField(
        max_digits=20, 
        decimal_places=4, 
        default=Decimal('0.0000'),  
        validators=[MinValueValidator(0)],
        blank=True,
        null=False
    )
    standard_time = models.DecimalField(
        max_digits=20, 
        decimal_places=6, 
        default=Decimal('0.000001'), 
        validators=[MinValueValidator(0.000001)]
    )
    price = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        default=Decimal('0.01'), 
        validators=[MinValueValidator(0.01)]
    )

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
                check=Q(department__in=ALLOWED_WAGON_DEPARTMENTS) | Q(type_wagon__isnull=True),
            ),
            # Ensure work_name is unique within the same department
            models.UniqueConstraint(
                fields=['department', 'work_name'],
                name='unique_work_name_per_department'
            ),
        ]

    def __str__(self):
        return self.work_name

    def clean(self):
        """
        Normalize and validate fields before saving:
        - If type_material is empty, set it to None and reset usage_material to 0.
        - Enforce business rule for type_wagon:
          only allowed for departments in ALLOWED_WAGON_DEPARTMENTS, else set to None.
        """
        if not self.type_material:
            self.type_material = None
            self.usage_material = Decimal('0.0000')

        if self.department not in ALLOWED_WAGON_DEPARTMENTS:
            self.type_wagon = None
        elif not self.type_wagon:
            self.type_wagon = None

    def save(self, *args, **kwargs):
        """
        Ensure the instance is valid and normalized before persisting:
        - Call full_clean() to run model/field validators and clean().
        - Then save to the database.
        """
        self.full_clean()
        return super().save(*args, **kwargs)
    