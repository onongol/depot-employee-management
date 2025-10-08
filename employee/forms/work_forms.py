from django import forms

from employee.models import Work
from employee.constants.constants import get_job_title_choices, TYPE_WAGON_CHOICES, ALLOWED_WAGON_DEPARTMENTS, EMPTY_SELECT


class WorkForm(forms.ModelForm):
    """Form for creating or updating a Work record."""
    def __init__(self, *args, **kwargs):
        """Initialize form and dynamically set job title and type_wagon choices based on department."""
        # Get the department from the keyword arguments
        department = kwargs.pop('department', None) 
        super().__init__(*args, **kwargs)
        dept = (
            department
            or (self.data.get('department') if self.is_bound else None)
            or getattr(self.instance, 'department', None)
        )
        self.fields['job_title'].choices = get_job_title_choices(dept) 

        # Dynamically set type_wagon choices based on department
        if dept in set(ALLOWED_WAGON_DEPARTMENTS):
            self.fields['type_wagon'].choices = EMPTY_SELECT + list(TYPE_WAGON_CHOICES)
            self.fields['type_wagon'].initial = None
        else:
            # Show empty select (not required) and ensure None
            self.fields['type_wagon'].choices = EMPTY_SELECT
            self.fields['type_wagon'].initial = None

    class Meta:
        model = Work
        fields = '__all__'
        widgets = {
            'job_title': forms.Select(attrs={'class': 'form-control'}),
            'work_name': forms.TextInput(attrs={'class': 'form-control'}),
            'type_wagon': forms.Select(attrs={'class': 'form-control'}),
            'type_material': forms.TextInput(attrs={'class': 'form-control'}),
            'usage_material': forms.NumberInput(
                attrs={
                    'class': 'form-control', 
                    'type': 'number', 
                    'min': '0',
                }
            ),
            'standard_time': forms.NumberInput(
                attrs={
                    'class': 'form-control', 
                    'type': 'number', 
                    'min': '0',
                    'value': '0.000000',
                    'step': '0.000001'
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control', 
                    'type': 'number', 
                    'min': '0',
                    'value': '0.00',
                    'step': '0.01'
                }
            ),
        }


class UpdateWorkForm(forms.ModelForm):
    """Form for updating an existing Work record."""
    def __init__(self, *args, **kwargs):
        """Initialize form and dynamically set job title and type_wagon choices based on department."""
        # Get the department from the keyword arguments
        department = kwargs.pop('department', None) 
        super().__init__(*args, **kwargs)
        dept = (
            department
            or (self.data.get('department') if self.is_bound else None)
            or getattr(self.instance, 'department', None)
        )
        self.fields['job_title'].choices = get_job_title_choices(dept) 

        # Dynamically set type_wagon choices based on department
        if dept in set(ALLOWED_WAGON_DEPARTMENTS):
            self.fields['type_wagon'].choices = EMPTY_SELECT + list(TYPE_WAGON_CHOICES)
            self.fields['type_wagon'].initial = None
        else:
            # Show empty select (not required) and ensure None
            self.fields['type_wagon'].choices = EMPTY_SELECT
            self.fields['type_wagon'].initial = None

    class Meta:
        model = Work
        fields = ['job_title', 'type_wagon', 'type_material', 'usage_material', 'standard_time', 'price']
        widgets = { 
            'job_title': forms.Select(attrs={'class': 'form-control'}),
            'type_wagon': forms.Select(attrs={'class': 'form-control'}),
            'type_material': forms.TextInput(attrs={'class': 'form-control'}),
            'usage_material': forms.NumberInput(attrs={
                'class': 'form-control', 
                'type': 'number',
                'min': '0',
                }
            ),
            'standard_time': forms.NumberInput(attrs={
                'class': 'form-control', 
                'type': 'number', 
                'min': '0',
                'step': '0.000001'
                }
            ),
            'price': forms.NumberInput(attrs={
                'class': 'form-control', 
                'type': 'number', 
                'min': '0',
                'step': '0.01'
                }
            ),
        }
