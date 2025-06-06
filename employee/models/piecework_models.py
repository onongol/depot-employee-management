from django.db import models
from django.core.validators import MinValueValidator
from datetime import date
from decimal import Decimal

from .employee_models import Employee
from .work_models import Work


class Piecework(models.Model):
    """Model to record the piecework done by employees."""
    record_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.RESTRICT)

    TYPE_WORK_CHOICES = [
        ('84', '84'),
        ('29', '29'),
        ('ТҮГ', 'ТҮГ'),
        ('Нөөц', 'Нөөц'),
        ('Завод', 'Завод'),
        ('Депо', 'Депо'),
    ]
    type_work = models.CharField(max_length=50, choices=TYPE_WORK_CHOICES)
    amount = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        default=Decimal('0.00'), 
        validators=[MinValueValidator(0.00)],
    )
    amount_price = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        default=Decimal('0.00'), 
        validators=[MinValueValidator(0.00)], 
        editable=False
    )
    amount_material = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        default=Decimal('0.00'), 
        validators=[MinValueValidator(0.00)], 
        editable=False
    )
    work_date = models.DateField(default=date.today)
    record_date = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # self.amount_price = self.work.price * self.amount
        self.amount_material = self.work.usage_material * self.amount
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.employee.name} - {self.work.work_name} - {self.type_work} on {self.work_date}"
