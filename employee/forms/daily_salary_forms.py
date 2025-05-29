from django import forms

from employee.models import DailySalary


class DailySalaryForm(forms.ModelForm):
    """Form for creating a new DailySalary record."""
    class Meta:
        model = DailySalary
        fields = '__all__'
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'hours_per_day': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0'}),
            'salary_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        error_messages = {
            'employee': {
                'required': 'Employee - Please select.',
            },
        }


class UpdateDailySalaryForm(forms.ModelForm):
    """Form for updating an existing DailySalary record (excludes employee)."""
    class Meta:
        model = DailySalary
        fields = ['hours_per_day', 'salary_date']
        widgets = {
            'hours_per_day': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'min': '0'}),
            'salary_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
