from datetime import date
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from simple_history.models import HistoricalRecords

from employee.constants.constants import (
    JOB_TITLE_CHOICES,
    TYPE_WAGON_CHOICES,
    TYPE_WORK_CHOICES,
)
from employee.models.models_mixins.display_mixins import (
    TypeWagonDisplayMixin,
    WagonNumberDisplayMixin,
)
from employee.models.work_models import Work
from employee.services.daily_work_calculations import (
    calculate_material_amount,
    calculate_price_amount,
    calculate_time_amount,
)
from employee.services.daily_work_sync import sync_piecework_with_dailywork
from employee.services.normalizes import (
    normalize_field,
    normalize_str_field,
)
from employee.services.snapshots import snapshot_attr


class DailyWork(TypeWagonDisplayMixin, WagonNumberDisplayMixin, models.Model):
    """Aggregated daily work record (not per employee)."""

    id = models.AutoField(primary_key=True)

    work = models.ForeignKey(Work, on_delete=models.RESTRICT)
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
    job_title = models.CharField(
        max_length=255,
        choices=JOB_TITLE_CHOICES,
        blank=False,
        null=False,
        db_index=True,
    )
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
        default=Decimal("0.01"),
        validators=[MinValueValidator(0.01)],
    )
    amount_time = models.DecimalField(
        max_digits=20,
        decimal_places=6,
        default=Decimal("0.000001"),
        validators=[MinValueValidator(0.000001)],
        editable=False,
    )
    amount_price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal("0.01"),
        validators=[MinValueValidator(0.01)],
        editable=False,
    )
    amount_material = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        default=Decimal("0.0000"),
        validators=[MinValueValidator(0)],
        editable=False,
    )
    work_date = models.DateField(default=date.today)
    record_date = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.work.work_name} ({self.type_work}) - {self.work_date}"

    def get_update_url(self):
        return reverse("daily_work_update", args=[self.pk])

    def get_dom_attrs(self):
        return {
            "data-work-name": self.work_name,
            "data-type-work": self.type_work,
            "data-work-date": self.work_date.isoformat(),
            "data-row-id": self.pk,
            "data-row-name": str(self),
            "data-edit-url": self.get_update_url(),
        }

    def save(self, *args, **kwargs):
        """
        Override save to:
        - Normalize inputs (wagon_number, job_title, type_wagon).
        - Snapshot denormalized fields from Work (work_name, department) for reporting stability.
        - Compute derived amounts (time, material, price) based on Work settings and quantity.
        - Persist the record, then synchronize related Piecework entries.

        This ensures consistent domain data and keeps downstream exports/reports robust.
        """
        self.work_name = snapshot_attr(self.work, "work_name")
        self.department = snapshot_attr(self.work, "department")
        self.job_title = normalize_field(self.job_title, self.work, "job_title")
        self.type_wagon = normalize_field(None, self.work, "type_wagon")
        self.wagon_number = normalize_str_field(self.wagon_number)

        self.amount_time = calculate_time_amount(self.work, self.amount or Decimal("0"))
        self.amount_material = calculate_material_amount(
            self.work, self.amount or Decimal("0")
        )
        self.amount_price = calculate_price_amount(
            self.work, self.amount or Decimal("0")
        )

        # Save the DailyWork instance
        super().save(*args, **kwargs)

        # --- After saving DailyWork, update related Piecework.amount_price ---
        sync_piecework_with_dailywork(self)
