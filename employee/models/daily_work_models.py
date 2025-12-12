from datetime import date
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from employee.constants.constants import (DEFAULT_WAGON_NUMBER,
                                          DEFAULT_WAGON_TYPE,
                                          JOB_TITLE_CHOICES,
                                          TYPE_WAGON_CHOICES,
                                          TYPE_WORK_CHOICES)
from employee.models.work_models import Work
from employee.services.daily_work_sync import sync_piecework_with_dailywork


class DailyWork(models.Model):
    """Aggregated daily work record (not per employee)."""
    job_title = models.CharField(
        max_length=255,
        choices=JOB_TITLE_CHOICES,
        blank=False,
        null=False,
        db_index=True,
    )
    work = models.ForeignKey(
        Work, 
        on_delete=models.RESTRICT
    )
    work_name = models.CharField(
        max_length=255,
        blank=True,
        null=False,
        editable=False,
        db_index=True,
    )
    department = models.CharField(
        max_length=255,
        blank=True,
        null=False,
        editable=False,
        db_index=True,
    )
    type_work = models.CharField(
        max_length=50, 
        choices=TYPE_WORK_CHOICES
    )
    wagon_number = models.CharField(
        max_length=50, 
        blank=True, 
        null=True
    )
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
    work_date = models.DateField(
        default=date.today
    )
    record_date = models.DateTimeField(
        auto_now_add=True
    )
    
    def save(self, *args, **kwargs):
        """
        Override save to calculate amount_time and amount_material.
        Also updates related Piecework entries after saving.
        """
        # Set wagon_number to None if empty
        if not self.wagon_number:
            self.wagon_number = None

        # Set job_title and type_wagon from Work if not set
        if self.work:
            if not self.job_title:
                self.job_title = self.work.job_title
            # Always normalize type_wagon: only keep if present, else None
            self.type_wagon = self.work.type_wagon or None

        # Snapshot work_name and department from related Work
            try:
                self.work_name = getattr(self.work, 'work_name', None)
                self.department = getattr(self.work, 'department', None)
            except Exception:
                self.work_name = None
                self.department = None

        # Calculate amount_time
        std_time = getattr(self.work, 'standard_time', None)
        std_time_dec = Decimal(str(std_time or 0))
        amt = self.amount or Decimal('0.000000')
        self.amount_time = (std_time_dec * amt).quantize(Decimal('0.000000'))
        
        # Calculate amount_material
        self.amount_material = self.work.usage_material * self.amount

        # Calculate amount_price
        price = getattr(self.work, 'price', None)
        price_dec = Decimal(str(price or 0))
        self.amount_price = (price_dec * amt).quantize(Decimal('0.00'))

        # Save the DailyWork instance
        super().save(*args, **kwargs)

        # --- After saving DailyWork, update related Piecework.amount_price ---
        sync_piecework_with_dailywork(self)
    
    @property
    def wagon_number_display(self):
        # Return default if wagon_number is not set
        return DEFAULT_WAGON_NUMBER if not self.wagon_number else self.wagon_number
    
    @property
    def type_wagon_display(self):
        # Prefer stored snapshot; fallback to default symbol
        return self.type_wagon or DEFAULT_WAGON_TYPE
    
    def __str__(self):
        """String representation of the DailyWork model."""
        return f"{self.work.work_name}/{self.type_work}/{self.work_date}"
