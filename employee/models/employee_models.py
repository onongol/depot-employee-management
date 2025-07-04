from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum


class Employee(models.Model):
    """This model represents an employee in the system."""
    DEPARTMENT_CHOICES = [
        ('Механик', 'Механик'),
        ('Авто хяналтын бүс (АКП)', 'Авто хяналтын бүс (АКП)'),
        ('Засвар 1', 'Засвар 1'),
        ('Засвар 2', 'Засвар 2'),
        ('Хос дугуй', 'Хос дугуй'),
        ('Тэргэнцэр', 'Тэргэнцэр'),
        ('Автоугсраа', 'Авто угсраа'),
    ]

    RANK_CHOICES = [
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
    ]

    rank_to_money = {
        3: 8448.55, 
        4: 9616.24, 
        5: 11127.36, 
        6: 13187.98
    }

    employee_id = models.IntegerField(
        primary_key=True, 
        null=False, 
        validators=[MinValueValidator(1)], 
        unique=True
        )
    name = models.CharField(max_length=255)
    department = models.CharField(
        max_length=255, 
        choices=DEPARTMENT_CHOICES, 
    )
    job_title = models.CharField(
        max_length=255, 
        blank=False, 
        null=True
    )  
    rank = models.IntegerField(
        default=3, 
        null=False, 
        choices=RANK_CHOICES
    )
    money_per_hour = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        null=False, 
        editable=False
    )
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.money_per_hour = self.rank_to_money.get(self.rank, 8448.55)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_id}/{self.name}"
    
    def get_total_salary_day(self, month, year):
        """Calculate total salary for the employee for a given month and year."""
        return (
            self.dailysalary_set.filter(salary_date__month=month, salary_date__year=year)
            .aggregate(total=Sum('salary_day'))['total'] or 0
        )

    def get_total_piecework_amount(self, month, year):
        """Calculate total piecework amount for the employee for a given month and year."""
        from employee.models import Piecework
        return (
            Piecework.objects.filter(
                employee=self,
                work_date__month=month,
                work_date__year=year
            ).aggregate(total=Sum('amount_price'))['total'] or 0
        )

    def get_total_salary(self, month, year):
        """Calculate total salary including piecework for the employee for a given month and year."""
        return round(self.get_total_salary_day(month, year) + self.get_total_piecework_amount(month, year), 2)
