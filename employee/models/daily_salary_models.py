from datetime import date
from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from employee.models.employee_models import Employee


class DailySalary(models.Model):
    """Model to record daily salary for employees."""

    salary_id = models.AutoField(primary_key=True, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
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
        db_index=True,
    )
    hours_per_day = models.IntegerField(
        default=11, validators=[MinValueValidator(1), MaxValueValidator(24)]
    )
    salary_day = models.DecimalField(
        max_digits=20, decimal_places=2, default=Decimal("0.00"), editable=False
    )
    salary_date = models.DateField(default=date.today)
    record_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """ "
        Model-level metadata:
        - Enforces a unique constraint on (employee, salary_date) to prevent
        multiple DailySalary records for the same employee on the same date.
        """

        constraints = [
            models.UniqueConstraint(
                fields=["employee", "salary_date"], name="unique_employee_salary_date"
            )
        ]

    def __str__(self):
        return f"(ID: {self.employee.employee_id}) {self.employee.name} - {self.salary_date}"
    
    def get_update_url(self):
        return reverse("daily_salary_update", args=[self.pk])

    def save(self, *args, **kwargs):
        """
        Override save to:
        - Snapshot employee_name and department from the related Employee for stable reporting.
        - Validate that employee.money_per_hour is present.
        - Compute salary_day (hours_per_day * money_per_hour) before persisting.

        This keeps denormalized fields consistent and ensures salary calculations
        are stored with each record for simpler exports and historical accuracy.
        """
        if self.employee:
            self.employee_name = self.employee.name

        if self.employee.money_per_hour is None:
            raise ValueError(
                _("Cannot save: hourly rate is not set for this employee.")
            )

        self.salary_day = Decimal(self.hours_per_day) * self.employee.money_per_hour

        super().save(*args, **kwargs)
