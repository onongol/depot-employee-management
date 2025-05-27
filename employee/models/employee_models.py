from django.db import models
from django.core.validators import MinValueValidator


class Employee(models.Model):
    employee_id = models.IntegerField(
        primary_key=True, 
        null=False, 
        validators=[MinValueValidator(1)], 
        unique=True
        )
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=False, null=True)
    job_title = models.CharField(max_length=255, blank=False, null=True)
    
    RANK_CHOICES = [
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
    ]
    rank = models.IntegerField(default=3, null=False, choices=RANK_CHOICES)
    money_per_hour = models.DecimalField(max_digits=10, decimal_places=2, null=False, editable=False)

    rank_to_money = {3: 8448.55, 4: 9616.24, 5: 11127.36, 6: 13187.98}

    def save(self, *args, **kwargs):
        self.money_per_hour = self.rank_to_money.get(self.rank, 8448.55)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Id: {self.employee_id} / {self.name}"
