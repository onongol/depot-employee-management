from django import forms

from employee.models import DailyPay

class DailyPayForm(forms.ModelForm):
    """Form for creating a new DailyPay record."""
    class Meta:
        model = DailyPay
        fields = '__all__'
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'hours_per_day': forms.NumberInput(
                attrs={
                    'class': 'form-control', 
                    'type': 'number', 
                    'min': '0',
                    'max': '24'
                }
            ),
            'salary_date': forms.DateInput(
                attrs={
                    'class': 'form-control', 
                    'type': 'date'
                }
            ),
        }


class UpdateDailyPayForm(forms.ModelForm):
    """Form for updating an existing DailyPay record (excludes employee)."""
    class Meta:
        model = DailyPay
        fields = ['hours_per_day', 'salary_date']
        widgets = {
            'hours_per_day': forms.NumberInput(
                attrs={
                    'class': 'form-control', 
                    'type': 'number', 
                    'min': '0',
                    'max': '24'
                }
            ),
            'salary_date': forms.DateInput(
                attrs={
                    'class': 'form-control', 
                    'type': 'date'
                }
            ),
        }
