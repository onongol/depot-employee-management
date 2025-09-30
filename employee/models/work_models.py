from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

from employee.constants.constants import DEFAULT_MATERIAL_TYPE


class Work(models.Model):
    """This model represents a work item in the system."""
    work_id = models.AutoField(primary_key=True, editable=False)
    department = models.CharField(
        max_length=255, 
        blank=False, 
        null=False
    )
    job_title = models.CharField(
        max_length=255, 
        blank=False, 
        null=False
    )
    work_name = models.CharField(max_length=255, unique=True)
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

    def save(self, *args, **kwargs):
        """
        Save the Work instance.
        If material is not specified, set default values.
        """
        if not self.type_material:
            self.type_material = None
            self.usage_material = Decimal('0.0000')
        super().save(*args, **kwargs)

    @property
    def type_material_display(self):
        return DEFAULT_MATERIAL_TYPE if not self.type_material else self.type_material

    def __str__(self):
        return self.work_name
