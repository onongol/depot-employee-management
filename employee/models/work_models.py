from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Work(models.Model):
    """This model represents a work item in the system."""
    work_id = models.AutoField(primary_key=True, editable=False)
    department = models.CharField(max_length=255, blank=False, null=True)
    work_name = models.CharField(max_length=255, unique=True)
    type_material = models.CharField(max_length=255, blank=True, null=True)
    usage_material = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),  
        validators=[MinValueValidator(0.00)]
        )
    standard_time = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'), 
        validators=[MinValueValidator(0.01)])
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'), 
        validators=[MinValueValidator(0.01)]
        )

    def __str__(self):
        return self.work_name