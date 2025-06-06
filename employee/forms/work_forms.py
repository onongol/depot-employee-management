from django import forms

from employee.models import Work


class WorkForm(forms.ModelForm):
    """Form for creating or updating a Work record."""
    class Meta:
        model = Work
        fields = '__all__'
        widgets = {
            'work_name': forms.TextInput(attrs={'class': 'form-control'}),
            'type_material': forms.TextInput(attrs={'class': 'form-control'}),
            'usage_material': forms.NumberInput(
                attrs={
                    'class': 'form-control', 
                    'type': 'number', 
                    'min': '0.00'
                }
            ),
            'standard_time': forms.NumberInput(
                attrs={
                    'class': 'form-control', 
                    'type': 'number', 
                    'min': '0.0000'
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control', 
                    'type': 'number', 
                    'min': '0.00'
                }
            ),
        }


class UpdateWorkForm(forms.ModelForm):
    """Form for updating an existing Work record."""
    class Meta:
        model = Work
        fields = ['type_material', 'usage_material', 'standard_time', 'price']
        widgets = { 
            'type_material': forms.TextInput(attrs={'class': 'form-control'}),
            'usage_material': forms.NumberInput(attrs={
                'class': 'form-control', 
                'type': 'number', 
                'min': '0.00'
                }
            ),
            'standard_time': forms.NumberInput(attrs={
                'class': 'form-control', 
                'type': 'number', 
                'min': '0.0000'
                }
            ),
            'price': forms.NumberInput(attrs={
                'class': 'form-control', 
                'type': 'number', 
                'min': '0.00'
                }
            ),
        }
