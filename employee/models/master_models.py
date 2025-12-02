from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

from employee.constants.constants import DEPARTMENT_CHOICES


class Master(models.Model):
    """This model represents a master in the system."""
    master_id = models.IntegerField(
        primary_key=True,
        null=False, 
        validators=[MinValueValidator(1)], 
        unique=True
    )
    name = models.CharField(
        max_length=255
    )
    department = models.CharField(
        max_length=255, 
        choices=DEPARTMENT_CHOICES
    )

    # Active status of the employee
    is_active = models.BooleanField(
        default=True
    )

    # Connection to the User model
    user = models.OneToOneField(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='master_profile'
    )

    def __str__(self):
        """String representation of the Master model."""
        return f"{self.master_id}/{self.name}"
