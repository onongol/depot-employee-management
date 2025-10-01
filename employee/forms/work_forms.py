from django import forms

from employee.models import Work
from employee.constants.constants import get_job_title_choices


class WorkForm(forms.ModelForm):
    """Form for creating or updating a Work record."""
    def __init__(self, *args, **kwargs):
        """Initialize form and dynamically set job title choices based on department."""
        department = kwargs.pop('department', None) 
        super().__init__(*args, **kwargs)
        dept = (
            department
            or (self.data.get('department') if self.is_bound else None)
            or getattr(self.instance, 'department', None)
        )
        self.fields['job_title'].choices = get_job_title_choices(dept) 

    class Meta:
        model = Work
        fields = '__all__'
        widgets = {
            'job_title': forms.Select(attrs={'class': 'form-control'}),
            'work_name': forms.TextInput(attrs={'class': 'form-control'}),
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
        """Initialize form and dynamically set job title choices based on department."""
        department = kwargs.pop('department', None) 
        super().__init__(*args, **kwargs)
        dept = (
            department
            or (self.data.get('department') if self.is_bound else None)
            or getattr(self.instance, 'department', None)
        )
        self.fields['job_title'].choices = get_job_title_choices(dept) 

    class Meta:
        model = Work
        fields = ['job_title', 'type_material', 'usage_material', 'standard_time', 'price']
        widgets = { 
            'job_title': forms.Select(attrs={'class': 'form-control'}),
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
