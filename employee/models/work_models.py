from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q

from employee.constants.constants import (ALLOWED_WAGON_DEPARTMENTS,
                                          DEFAULT_MATERIAL_TYPE,
                                          DEFAULT_WAGON_TYPE,
                                          JOB_TITLE_CHOICES,
                                          TYPE_WAGON_CHOICES)


class Work(models.Model):
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
        default=Decimal('0.000000'), 
        validators=[MinValueValidator(0)]
    )
    price = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        default=Decimal('0.00'), 
        validators=[MinValueValidator(0)]
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
        # Normalize empty strings -> None
        if not self.type_material:
            self.type_material = None
            self.usage_material = Decimal('0.0000')

        if self.department not in ALLOWED_WAGON_DEPARTMENTS:
            self.type_wagon = None
        elif not self.type_wagon:
            self.type_wagon = None

    def save(self, *args, **kwargs):
        # Ensure clean is called before saving
        self.full_clean()
        return super().save(*args, **kwargs)
        
    @property
    def type_material_display(self):
        return self.type_material or DEFAULT_MATERIAL_TYPE

    @property
    def type_wagon_display(self):
        return self.type_wagon or DEFAULT_WAGON_TYPE
