from django import forms

from employee.models import DailyWork
from employee.constants.constants import get_type_work_choices


class TypeWorkChoiceMixin:
    """Mixin to set type work choices based on department."""
    def __init__(self, *args, **kwargs):
        department = kwargs.pop('department', None)
        super().__init__(*args, **kwargs)
        if 'type_work' in self.fields:
            self.fields['type_work'].choices = get_type_work_choices(department)


class DailyWorkForm(TypeWorkChoiceMixin, forms.ModelForm):
    """Form for creating a new DailyWork record."""
    class Meta:
        model = DailyWork
        fields = '__all__'
        widgets = {
            'work': forms.Select(attrs={
                'class': 'form-control'
                }
            ),
            'type_work': forms.Select(attrs={
                'class': 'form-control'
                }
            ),
            'wagon_number': forms.TextInput(attrs={
                'class': 'form-control', 
                'type': 'text', 
                }
            ),
            'work_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
                }
            ),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 
                'type': 'number', 
                'min': '0'
                }
            ),
        }        
        

class UpdateDailyWorkForm(TypeWorkChoiceMixin, forms.ModelForm):
    """Form for updating an existing DailyWork record."""
    class Meta:
        model = DailyWork
        fields = ['type_work', 'wagon_number', 'amount', 'work_date']
        widgets = {
            'type_work': forms.Select(attrs={
                'class': 'form-control'
                }
            ),
            'wagon_number': forms.TextInput(attrs={
                'class': 'form-control', 
                'type': 'text', 
                }
            ),
            'work_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
                }
            ),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 
                'type': 'number', 
                'min': '0'
                }
            ),
        }
