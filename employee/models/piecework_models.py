from datetime import date
from decimal import Decimal
from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models

from employee.constants.constants import (JOB_TITLE_CHOICES,
                                          TYPE_WAGON_CHOICES,
                                          TYPE_WORK_CHOICES)
from employee.models import DailyWork, Employee, Work
from employee.models.models_mixins.display_mixins import (TypeWagonDisplayMixin, 
                                                          WagonNumberDisplayMixin)
from employee.services.daily_work_canculate import (canculate_amount_material,
                                                    canculate_amount_time)
from employee.services.snapshots import (snapshot_employee_name,
                                         snapshot_work_name,
                                         snapshot_department)


class Piecework(TypeWagonDisplayMixin, WagonNumberDisplayMixin, models.Model):
    """Model to record the piecework done by employees."""
    TYPE_WORK_CHOICES = TYPE_WORK_CHOICES

    # Link to DailyWork for aggregation
    daily_work = models.ForeignKey(
        DailyWork,
        on_delete=models.CASCADE,  # Cascade delete to remove associated piecework records
        related_name='pieceworks',  # For reverse access: daily_work.pieceworks.all()
        null=True,
        blank=True
    )
    record_id = models.AutoField(
        primary_key=True
    )
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE
    )
    employee_name = models.CharField(
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
    group_id = models.CharField(
        max_length=36, 
        blank=True, 
        null=True, 
        db_index=True
    )

    def __str__(self):
        return f"{self.employee.employee_id}/{self.employee.name}/{self.work.work_name}/{self.type_work}/{self.work_date}"
    
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

        # Snapshot
        if self.employee:
            self.employee_name = snapshot_employee_name(self.employee)
            self.department = snapshot_department(self.employee)

        if self.work:
            self.work_name = snapshot_work_name(self.work)

        self.amount_time = canculate_amount_time(self.work, self.amount or Decimal('0'))
        self.amount_material = canculate_amount_material(self.work, self.amount or Decimal('0'))

        super().save(*args, **kwargs)
