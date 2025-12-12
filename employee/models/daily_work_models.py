from datetime import date
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from employee.constants.constants import (JOB_TITLE_CHOICES,
                                          TYPE_WAGON_CHOICES,
                                          TYPE_WORK_CHOICES)
from employee.models.work_models import Work
from employee.models.models_mixins.display_mixins import (TypeWagonDisplayMixin,
                                                          WagonNumberDisplayMixin)
from employee.services.daily_work_sync import sync_piecework_with_dailywork
from employee.services.daily_work_canculate import (canculate_amount_time,
                                                    canculate_amount_material,
                                                    canculate_amount_price)
from employee.services.snapshots import (snapshot_work_name,
                                         snapshot_department)


class DailyWork(TypeWagonDisplayMixin, WagonNumberDisplayMixin, models.Model):
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

    def __str__(self):
        return f"{self.work.work_name}/{self.type_work}/{self.work_date}"
    
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

            # Snapshot
            self.work_name = snapshot_work_name(self.work)
            self.department = snapshot_department(self.work)

        self.amount_time = canculate_amount_time(self.work, self.amount or Decimal('0'))
        self.amount_material = canculate_amount_material(self.work, self.amount or Decimal('0'))
        self.amount_price = canculate_amount_price(self.work, self.amount or Decimal('0'))

        # Save the DailyWork instance
        super().save(*args, **kwargs)

        # --- After saving DailyWork, update related Piecework.amount_price ---
        sync_piecework_with_dailywork(self)
