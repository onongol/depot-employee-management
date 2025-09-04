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
                    'min': '0',
                    'value': '0.0000',
                    'step': '0.0001',
                }
            ),
            'standard_time': forms.NumberInput(
                attrs={
                    'class': 'form-control', 
                    'type': 'number', 
                    'min': '0',
                    'value': '0.000000',
                    'step': '0.000001',
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control', 
                    'type': 'number', 
                    'min': '0',
                    'value': '0.00',
                    'step': '0.01',
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
                'min': '0',
                'step': '0.0001'
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
