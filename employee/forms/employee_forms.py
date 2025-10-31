import re
from django import forms
from django.utils.translation import gettext_lazy as _

from employee.models import Employee
from employee.constants.constants import get_job_title_choices


class EmployeeForm(forms.ModelForm):
    """Form to create a new employee."""
    def __init__(self, *args, **kwargs):
        """Initialize form and dynamically set job title choices based on department."""
        super().__init__(*args, **kwargs)
        dept = (self.data.get('department') if self.is_bound else None) or self.initial.get('department')
        self.fields['job_title'].choices = get_job_title_choices(dept)

    def clean_name(self):
        """Validate name format: one letter, dot, name (e.g. L.Name)."""
        name = self.cleaned_data['name']
        if not re.match(r'^[А-ЯA-Z]\.[А-Яа-яA-Za-zЁёҮүӨөҮүӨө]+$', name):
            raise forms.ValidationError(
                _("Name must be in the format: L.Name (e.g. D.Sukhbaatar)!")
            )
        return name

    class Meta:
        model = Employee
        fields = ['employee_id', 'name', 'department', 'job_title', 'rank', 'money_per_hour']
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
            'money_per_hour': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': '0',
                'step': '0.01'
            }),
        }


class UpdateEmployeeForm(forms.ModelForm):
    """Form to update employee details, excluding employee_id."""
    def __init__(self, *args, **kwargs):
        """Initialize form and dynamically set job title choices based on department."""
        super().__init__(*args, **kwargs)
        dept = (self.data.get('department') if self.is_bound else None) or self.initial.get('department')
        self.fields['job_title'].choices = get_job_title_choices(dept)

    def clean_name(self):
        """Validate name format: one letter, dot, name (e.g. L.Name)."""
        name = self.cleaned_data['name']
        if not re.match(r'^[А-ЯA-Z]\.[А-Яа-яA-Za-zЁёҮүӨөҮүӨө]+$', name):
            raise forms.ValidationError(
                _("Name must be in the format: L.Name (e.g. D.Sukhbaatar)!")
            )
        return name

    class Meta:
        model = Employee
        fields = ['name', 'job_title', 'rank', 'money_per_hour']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.Select(attrs={'class': 'form-control'}),
            'rank': forms.Select(attrs={'class': 'form-control'}),
            'money_per_hour': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': '0',
                'step': '0.01'
            }),
        }
