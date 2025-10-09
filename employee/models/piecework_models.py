from django.db import models
from django.core.validators import MinValueValidator
from datetime import date
from decimal import Decimal
from uuid import uuid4

from .employee_models import Employee
from .work_models import Work
from employee.constants.constants import TYPE_WORK_CHOICES, DEFAULT_WAGON_NUMBER, JOB_TITLE_CHOICES, TYPE_WAGON_CHOICES, DEFAULT_WAGON_TYPE


class Piecework(models.Model):
    """Model to record the piecework done by employees."""

    TYPE_WORK_CHOICES = TYPE_WORK_CHOICES
    
    record_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    job_title = models.CharField(
        max_length=255,
        choices=JOB_TITLE_CHOICES,
        blank=False,
        null=False,
        db_index=True,
    )

    work = models.ForeignKey(Work, on_delete=models.RESTRICT)
    type_work = models.CharField(max_length=50, choices=TYPE_WORK_CHOICES)
    wagon_number = models.CharField(max_length=50, blank=True, null=True)

    type_wagon = models.CharField(
        max_length=100,
        choices=TYPE_WAGON_CHOICES,
        blank=True,
        null=True,
        db_index=True,
    )

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

        if not self.wagon_number:
            self.wagon_number = None

        # Snapshot job_title & type_wagon from Work if missing
        if self.work:
            if not self.job_title:
                self.job_title = self.work.job_title
            # Always normalize type_wagon: only keep if present, else None
            self.type_wagon = self.work.type_wagon or None

        std_time = getattr(self.work, 'standard_time', None)
        std_time_dec = Decimal(str(std_time or 0))
        amt = self.amount or Decimal('0.000000')
        self.amount_time = (std_time_dec * amt).quantize(Decimal('0.000000'))
        self.amount_material = self.work.usage_material * self.amount
        super().save(*args, **kwargs)
    
    @property
    def wagon_number_display(self):
        return DEFAULT_WAGON_NUMBER if not self.wagon_number else self.wagon_number
    
    @property
    def type_wagon_display(self):
        # Prefer stored snapshot; fallback to default symbol
        return self.type_wagon or DEFAULT_WAGON_TYPE

    def __str__(self):
        return f"{self.employee.employee_id}/{self.employee.name}/{self.work.work_name}/{self.type_work}/{self.work_date}"
