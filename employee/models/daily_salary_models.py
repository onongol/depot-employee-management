from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from decimal import Decimal

from .employee_models import Employee


class DailySalary(models.Model):
    """Model to record daily salary for employees."""
    salary_id = models.AutoField(primary_key=True, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    hours_per_day = models.IntegerField(
        default=11,
        validators=[MinValueValidator(0), MaxValueValidator(24)]
    )
    salary_day = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal('0.00'),
        editable=False
    )
    salary_date = models.DateField(default=date.today)
    record_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure that the employee's money_per_hour is not None
        if self.employee.money_per_hour is None:
            raise ValueError("Employee's money_per_hour must not be None")
        self.salary_day = Decimal(self.hours_per_day) * self.employee.money_per_hour
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employee', 'salary_date'], name='unique_employee_salary_date')
        ]

    def __str__(self):
        return f"{self.employee.employee_id}/{self.employee.name}/{self.salary_date}"
