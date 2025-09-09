from django.db import models
from django.core.validators import MinValueValidator
from datetime import date
from decimal import Decimal
from uuid import uuid4

from .employee_models import Employee
from .work_models import Work
from employee.constants.constants import TYPE_WORK_CHOICES


class Piecework(models.Model):
    """Model to record the piecework done by employees."""

    TYPE_WORK_CHOICES = TYPE_WORK_CHOICES
    
    record_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.RESTRICT)
    type_work = models.CharField(max_length=50, choices=TYPE_WORK_CHOICES)
    wagon_number = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2, 
        default=Decimal('0.00'), 
        validators=[MinValueValidator(0)],
    )
    amount_time = models.DecimalField(
        max_digits=20,
        decimal_places=6,
        default=Decimal('0.000000'),
        validators=[MinValueValidator(0)],
        editable=False,
    )
    amount_price = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        default=Decimal('0.00'), 
        validators=[MinValueValidator(0)], 
        editable=False
    )
    amount_material = models.DecimalField(
        max_digits=20, 
        decimal_places=4, 
        default=Decimal('0.0000'), 
        validators=[MinValueValidator(0)], 
        editable=False
    )
    work_date = models.DateField(default=date.today)
    record_date = models.DateTimeField(auto_now_add=True)
    group_id = models.CharField(max_length=36, blank=True, null=True, db_index=True)
    
    def save(self, *args, **kwargs):
        """
        Save the Piecework instance.
        Generate group_id if not set.
        """
        if not self.group_id:
            self.group_id = str(uuid4())
        std_time = getattr(self.work, 'standard_time', None)
        std_time_dec = Decimal(str(std_time or 0))
        amt = self.amount or Decimal('0.000000')
        self.amount_time = (std_time_dec * amt).quantize(Decimal('0.000000'))
        self.amount_material = self.work.usage_material * self.amount
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.employee.employee_id}/{self.employee.name}/{self.work.work_name}/{self.type_work}/{self.work_date}"
