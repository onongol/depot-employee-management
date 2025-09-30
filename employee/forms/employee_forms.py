from django import forms

from employee.models import Employee


class EmployeeForm(forms.ModelForm):
    """Form to create a new employee."""
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
    class Meta:
        model = Employee
        fields = ['name', 'job_title', 'rank']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.Select(attrs={'class': 'form-control'}),
            'rank': forms.Select(attrs={'class': 'form-control'}),
        }
