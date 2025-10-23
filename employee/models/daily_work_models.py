import logging
from datetime import date
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator

from .work_models import Work
from employee.constants.constants import  JOB_TITLE_CHOICES, TYPE_WORK_CHOICES, TYPE_WAGON_CHOICES, DEFAULT_WAGON_TYPE, DEFAULT_WAGON_NUMBER


class DailyWork(models.Model):
    """
    Aggregated daily work record (not per employee).
    """
    job_title = models.CharField(
        max_length=255,
        choices=JOB_TITLE_CHOICES,
        blank=False,
        null=False,
        db_index=True,
    )
    work = models.ForeignKey(
        Work, 
        on_delete=models.RESTRICT
    )
    type_work = models.CharField(
        max_length=50, 
        choices=TYPE_WORK_CHOICES
    )
    wagon_number = models.CharField(
        max_length=50, 
        blank=True, 
        null=True
    )
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
        default=Decimal('0.00'), 
        validators=[MinValueValidator(0)],
    )
    amount_time = models.DecimalField(
        max_digits=20,
        decimal_places=6,
        default=Decimal('0.000000'),
        validators=[MinValueValidator(0)],
        editable=False,
    )
    amount_price = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        default=Decimal('0.00'), 
        validators=[MinValueValidator(0)], 
        editable=False
    )
    amount_material = models.DecimalField(
        max_digits=20, 
        decimal_places=4, 
        default=Decimal('0.0000'), 
        validators=[MinValueValidator(0)], 
        editable=False
    )
    work_date = models.DateField(
        default=date.today
    )
    record_date = models.DateTimeField(
        auto_now_add=True
    )
    
    def save(self, *args, **kwargs):
        """
        Override save to calculate amount_time and amount_material.
        Also updates related Piecework entries after saving.
        """
        # Set wagon_number to None if empty
        if not self.wagon_number:
            self.wagon_number = None

        # Set job_title and type_wagon from Work if not set
        if self.work:
            if not self.job_title:
                self.job_title = self.work.job_title
            # Always normalize type_wagon: only keep if present, else None
            self.type_wagon = self.work.type_wagon or None

        # Calculate amount_time
        std_time = getattr(self.work, 'standard_time', None)
        std_time_dec = Decimal(str(std_time or 0))
        amt = self.amount or Decimal('0.000000')
        self.amount_time = (std_time_dec * amt).quantize(Decimal('0.000000'))
        
        # Calculate amount_material
        self.amount_material = self.work.usage_material * self.amount

        # Calculate amount_price
        price = getattr(self.work, 'price', None)
        price_dec = Decimal(str(price or 0))
        self.amount_price = (price_dec * amt).quantize(Decimal('0.00'))

        # Save the DailyWork instance
        super().save(*args, **kwargs)

        # --- After saving DailyWork, update related Piecework.amount_price ---
        try:
            # Local imports to avoid circular import issues
            from .piecework_models import Piecework
            from .daily_salary_models import DailySalary
            from employee.views.piecework.piecework_calculation import piecework_calculate_update

            # Get department from the related Work
            department = getattr(self.work, 'department', None)

            # Get all DailySalary entries for employees in the department on the work_date
            employees_salary = DailySalary.objects.filter(
                employee__department=department,
                salary_date=self.work_date
            )

            # Find all Piecework entries linked to this DailyWork
            related_pieceworks = Piecework.objects.filter(daily_work=self)

            for pw in related_pieceworks:
                # Synchronize fields from DailyWork to Piecework
                pw.type_work = self.type_work
                pw.wagon_number = self.wagon_number
                pw.amount = self.amount
                pw.work_date = self.work_date

                # Calculate amount_time for Piecework
                std_time = getattr(self.work, 'standard_time', None)
                std_time_dec = Decimal(str(std_time or 0))
                amt = pw.amount or Decimal('0.000000')
                pw.amount_time = (std_time_dec * amt).quantize(Decimal('0.000000'))

                # Get the DailySalary for the Piecework's employee on the work_date
                daily_salary = DailySalary.objects.filter(
                    employee=pw.employee,
                    salary_date=self.work_date
                ).first()

                # Recalculate amount_price    
                new_price = piecework_calculate_update(self.work, pw.amount, daily_salary, employees_salary)

                # Update amount_price if changed    
                if pw.amount_price != new_price:
                    pw.amount_price = new_price

                # Save the updated Piecework
                pw.save(update_fields=[
                    'type_work', 
                    'wagon_number', 
                    'amount',
                    'amount_time',
                    'amount_price',
                    'work_date', 
                ])

        except Exception as e:
            # Don't break primary save if update fails; log the problem
            logger = logging.getLogger(__name__)
            logger.exception("Failed updating related Piecework prices for DailyWork %s: %s", getattr(self, 'pk', None), str(e))
    
    @property
    def wagon_number_display(self):
        # Return default if wagon_number is not set
        return DEFAULT_WAGON_NUMBER if not self.wagon_number else self.wagon_number
    
    @property
    def type_wagon_display(self):
        # Prefer stored snapshot; fallback to default symbol
        return self.type_wagon or DEFAULT_WAGON_TYPE
    
    def __str__(self):
        return f"{self.work.work_name}/{self.type_work}/{self.work_date}"
