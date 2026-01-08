from django import forms
from django.utils.translation import gettext_lazy as _

from employee.models import Employee
from employee.forms.forms_mixins.employee_job_titel_mixins import JobTitleChoicesMixin
from employee.forms.forms_mixins.name_mixins import NameValidationMixin


class EmployeeForm(JobTitleChoicesMixin, NameValidationMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
                'min': '0.01',
                'step': '0.01'
            }),
        }


class UpdateEmployeeForm(NameValidationMixin, JobTitleChoicesMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
                'min': '0.01',
                'step': '0.01'
            }),
        }
