import re
from django import forms
from django.utils.translation import gettext_lazy as _

from employee.models import Employee
from employee.constants.constants import get_job_title_choices


class EmployeeFormMixin:
    """Mixin: set job_title choices based on department and provide clean_name."""
    def __init__(self, *args, department=None, **kwargs):
        # allow explicit department override via kwarg, otherwise try data/initial/instance
        super().__init__(*args, **kwargs)
        dept = department
        if dept is None:
            dept = (self.data.get('department') if getattr(self, 'is_bound', False) else None) \
                   or self.initial.get('department') \
                   or getattr(getattr(self, 'instance', None), 'department', None)
        if 'job_title' in self.fields:
            self.fields['job_title'].choices = get_job_title_choices(dept)

    def clean_name(self):
        """Validate name format: one letter, dot, name (e.g. L.Name)."""
        name = self.cleaned_data.get('name')
        if not name:
            return name
        pattern = r'^[А-ЯA-ZҮӨЁ]\.[А-ЯA-ZҮӨЁ][а-яa-zёүө]*(?:-[А-ЯA-ZҮӨЁ][а-яa-zёүө-]*)*$'
        if not re.match(pattern, name):
            raise forms.ValidationError(
                _("Name must be in the format: L.Name (e.g. D.Sukhbaatar or A.Gun-Aajav).")
            )
        return name


class EmployeeForm(EmployeeFormMixin, forms.ModelForm):
    """Form to create a new employee."""
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
                'min': '0',
                'step': '0.01'
            }),
        }


class UpdateEmployeeForm(EmployeeFormMixin, forms.ModelForm):
    """Form to update employee details, excluding employee_id."""
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
                'min': '0',
                'step': '0.01'
            }),
        }
