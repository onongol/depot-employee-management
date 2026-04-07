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
    normalize_job_title,
    normalize_type_wagon,
    normalize_wagon_number,
)
from employee.services.snapshots import (
    snapshot_department,
    snapshot_employee_name,
    snapshot_work_name,
)


class Piecework(TypeWagonDisplayMixin, WagonNumberDisplayMixin, models.Model):
    """Model to record the piecework done by employees."""

    TYPE_WORK_CHOICES = TYPE_WORK_CHOICES

    # Link to DailyWork for aggregation
    daily_work = models.ForeignKey(
        DailyWork,
        on_delete=models.CASCADE,  # Cascade delete to remove associated piecework records
        related_name="pieceworks",  # For reverse access: daily_work.pieceworks.all()
        null=True,
        blank=True,
    )
    record_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
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
        return f"(ID: {self.employee.employee_id}) {self.employee.name}, {self.work.work_name} ({self.type_work}) - {self.work_date}"

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
        if not self.group_id:
            self.group_id = str(uuid4())

        self.wagon_number = normalize_wagon_number(self.wagon_number)

        if self.work:
            self.job_title = normalize_job_title(self.job_title, self.work)
            self.type_wagon = normalize_type_wagon(self.work)

        if self.employee:
            self.employee_name = snapshot_employee_name(self.employee)
            self.department = snapshot_department(self.employee)

        if self.work:
            self.work_name = snapshot_work_name(self.work)

        self.amount_time = calculate_time_amount(self.work, self.amount or Decimal("0"))
        self.amount_material = calculate_material_amount(
            self.work, self.amount or Decimal("0")
        )

        super().save(*args, **kwargs)
