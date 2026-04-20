from datetime import date
from decimal import Decimal
from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models
from simple_history.models import HistoricalRecords

from employee.constants.constants import (
    JOB_TITLE_CHOICES,
    TYPE_WAGON_CHOICES,
    TYPE_WORK_CHOICES,
)
from employee.models import DailyWork, Employee, Work
from employee.models.models_mixins.display_mixins import (
    TypeWagonDisplayMixin,
    WagonNumberDisplayMixin,
)
from employee.services.daily_work_calculations import (
    calculate_material_amount,
    calculate_time_amount,
)
from employee.services.normalizes import (
    normalize_field,
    normalize_str_field,
)
from employee.services.snapshots import snapshot_attr


class Piecework(TypeWagonDisplayMixin, WagonNumberDisplayMixin, models.Model):
    """Model to record the piecework done by employees."""

    TYPE_WORK_CHOICES = TYPE_WORK_CHOICES

    id = models.AutoField(primary_key=True)

    daily_work = models.ForeignKey(
        DailyWork,
        on_delete=models.CASCADE,
        related_name="pieceworks",
        null=True,
        blank=True,
    )

    employee = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    employee_code = models.IntegerField(null=False, db_index=True, editable=False)
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

    work = models.ForeignKey(Work, on_delete=models.RESTRICT)
    work_name = models.CharField(
        max_length=255,
        blank=True,
        null=False,
        editable=False,
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
    group_id = models.CharField(max_length=36, blank=True, null=True, db_index=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"(ID: {self.employee.employee_id}) {self.employee.employee_name}, {self.work.work_name} ({self.type_work}) - {self.work_date}"

    def save(self, *args, **kwargs):
        """
        Override save to:
        - Normalize inputs (wagon_number, job_title, type_wagon).
        - Snapshot denormalized fields (employee_name, department, work_name) for stable reporting.
        - Compute derived amounts (time, material) based on Work settings and quantity.
        - Generate a group_id for batch operations if missing.
        - Persist the record.

        This ensures consistent domain data and keeps downstream exports/reports robust.
        """
        # Generate group_id if missing
        if not self.group_id:
            self.group_id = str(uuid4())

        self.employee_code = snapshot_attr(self.employee, "employee_id")
        self.employee_name = snapshot_attr(self.employee, "employee_name")
        self.department = snapshot_attr(self.employee, "department")
        self.job_title = normalize_field(self.job_title, self.work, "job_title")
        self.work_name = snapshot_attr(self.work, "work_name")
        self.type_wagon = normalize_field(None, self.work, "type_wagon")
        self.wagon_number = normalize_str_field(self.wagon_number)

        # Calculate derived amounts
        self.amount_time = calculate_time_amount(self.work, self.amount or Decimal("0"))
        self.amount_material = calculate_material_amount(
            self.work, self.amount or Decimal("0")
        )

        super().save(*args, **kwargs)
