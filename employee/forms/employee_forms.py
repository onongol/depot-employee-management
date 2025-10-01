from django import forms

from employee.models import Employee
from employee.constants.constants import get_job_title_choices


class EmployeeForm(forms.ModelForm):
    """Form to create a new employee."""
    def __init__(self, *args, **kwargs):
        """Initialize form and dynamically set job title choices based on department."""
        super().__init__(*args, **kwargs)
        dept = (self.data.get('department') if self.is_bound else None) or self.initial.get('department')
        self.fields['job_title'].choices = get_job_title_choices(dept)

    class Meta:
        model = Employee
        fields = ['employee_id', 'name', 'department', 'job_title', 'rank']
        widgets = {
            'employee_id': forms.NumberInput(
                attrs={
                    'class': 'form-control', 
                    'type': 'number', 
                    'min': '1'
                }
            ),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'job_title': forms.Select(attrs={'class': 'form-control'}),
            'rank': forms.Select(attrs={'class': 'form-control'}),
        }


class UpdateEmployeeForm(forms.ModelForm):
    """Form to update employee details, excluding employee_id."""
    def __init__(self, *args, **kwargs):
        """Initialize form and dynamically set job title choices based on department."""
        super().__init__(*args, **kwargs)
        dept = (self.data.get('department') if self.is_bound else None) or self.initial.get('department')
        self.fields['job_title'].choices = get_job_title_choices(dept)
        
    class Meta:
        model = Employee
        fields = ['name', 'job_title', 'rank']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.Select(attrs={'class': 'form-control'}),
            'rank': forms.Select(attrs={'class': 'form-control'}),
        }
