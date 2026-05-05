from datetime import date
from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from employee.models.employee_models import Employee


class DailySalary(models.Model):
    """Model to record daily salary for employees."""

    id = models.AutoField(primary_key=True, editable=False)

    employee = models.ForeignKey(Employee, models.RESTRICT)

    employee_code = models.IntegerField(null=False, db_index=True, editable=False)
    employee_name = models.CharField(
        max_length=255,
        blank=True,
        null=False,
        editable=False,  # This field is auto-populated from Employee.name
        db_index=True,
    )
    department = models.CharField(
        max_length=255,
        blank=True,
        null=False,
        editable=False,
    )
    job_title = models.CharField(
        max_length=255,
        blank=True,
        null=False,
        editable=False,
        db_index=True,
    )
    hours_per_day = models.IntegerField(
        default=11, validators=[MinValueValidator(1), MaxValueValidator(24)]
    )
    salary_day = models.DecimalField(
        max_digits=20, decimal_places=2, default=Decimal("0.00"), editable=False
    )
    salary_date = models.DateField(
        default=date.today,
        db_index=True,
    )
    salary_year = models.SmallIntegerField(null=True, editable=False)
    salary_month = models.SmallIntegerField(null=True, editable=False)
    record_date = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        """ "
        Model-level metadata:
        - Enforces a unique constraint on (employee, salary_date) to prevent
        multiple DailySalary records for the same employee on the same date.
        """

        indexes = [
            models.Index(fields=["department", "salary_date"]),
            models.Index(fields=["employee", "salary_year", "salary_month"]),
            models.Index(fields=["-record_date"]),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["employee", "salary_date"], name="unique_employee_salary_date"
            )
        ]

    def __str__(self):
        return f"(ID: {self.employee.employee_id}) {self.employee.employee_name} - {self.salary_date}"

    def get_update_url(self):
        return reverse("daily_salary_update", args=[self.pk])

    def get_dom_attrs(self):
        return {
            "data-emp-id": self.employee.employee_id,
            "data-emp-name": self.employee.employee_name,
            "data-salary-date": self.salary_date.isoformat(),
            "data-row-id": self.pk,
            "data-row-name": str(self),
            "data-edit-url": self.get_update_url(),
        }

    def save(self, *args, **kwargs):
        """
        Override save to:
        - Snapshot employee_name and department from the related Employee for stable reporting.
        - Validate that employee.money_per_hour is present.
        - Compute salary_day (hours_per_day * money_per_hour) before persisting.

        This keeps denormalized fields consistent and ensures salary calculations
        are stored with each record for simpler exports and historical accuracy.
        """
        self.employee_code = self.employee.employee_id
        self.employee_name = self.employee.employee_name
        self.department = self.employee.department
        self.job_title = self.employee.job_title

        if self.employee.money_per_hour is None:
            raise ValueError(
                _("Cannot save: hourly rate is not set for this employee.")
            )

        if self.salary_date:
            self.salary_year = self.salary_date.year
            self.salary_month = self.salary_date.month

        self.salary_day = Decimal(self.hours_per_day) * self.employee.money_per_hour

        super().save(*args, **kwargs)
