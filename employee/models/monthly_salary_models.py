from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from decimal import Decimal

from .employee_models import Employee


class MonthlySalary(models.Model):
    salary_id = models.AutoField(primary_key=True, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    hours_per_month = models.IntegerField(
        default=176, 
        validators=[MinValueValidator(0), MaxValueValidator(744)]
        )
    salary_month = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'), 
        editable=False
        )
    
    MONTH_CHOICES = [(i, f"{i:02d}") for i in range(1, 13)]
    YEAR_CHOICES = [(year, str(year)) for year in range(2024, date.today().year + 1)]

    month = models.IntegerField(default=date.today().month, choices=MONTH_CHOICES)
    year = models.IntegerField(default=date.today().year, choices=YEAR_CHOICES)
    record_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.salary_month = Decimal(self.hours_per_month) * self.employee.money_per_hour
        super().save(*args, **kwargs)

    class Meta:
        unique_together = (('employee', 'month', 'year'),)

    def __str__(self):
        return f"{self.employee.name} - {self.month}/{self.year}"
