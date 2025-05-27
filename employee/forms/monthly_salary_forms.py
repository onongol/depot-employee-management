from django import forms

from employee.models import MonthlySalary


class MonthlySalaryForm(forms.ModelForm):
    """Form for creating a new MonthlySalary record."""
    class Meta:
        model = MonthlySalary
        fields = '__all__'
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'hours_per_month': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0'}),
            'month': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.Select(attrs={'class': 'form-control'}),
        }

        error_messages = {
            'employee': {
                'required': 'Employee - Please select.',
            },
        }


class UpdateMonthlySalaryForm(forms.ModelForm):
    """Form for updating an existing MonthlySalary record (excludes employee)."""
    class Meta:
        model = MonthlySalary
        fields = ['hours_per_month', 'month', 'year']
        widgets = {
            'hours_per_month': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0'}),
            'month': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.Select(attrs={'class': 'form-control'}),
        }
