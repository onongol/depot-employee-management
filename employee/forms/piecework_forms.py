from django import forms

from employee.constants.constants import get_type_work_choices
from employee.models import Piecework


class TypeWorkChoiceMixin:
    """Mixin to set type work choices based on department."""
    def __init__(self, *args, **kwargs):
        department = kwargs.pop('department', None)
        super().__init__(*args, **kwargs)
        if 'type_work' in self.fields:
            self.fields['type_work'].choices = get_type_work_choices(department)


class PieceworkForm(TypeWorkChoiceMixin, forms.ModelForm):
    """Form for creating a new Piecework record."""
    class Meta:
        model = Piecework
        fields = '__all__'
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'work': forms.Select(attrs={'class': 'form-control'}),
            'type_work': forms.Select(attrs={'class': 'form-control'}),
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
        

class UpdatePieceworkForm(TypeWorkChoiceMixin, forms.ModelForm):
    """Form for updating an existing Piecework record."""
    class Meta:
        model = Piecework
        fields = ['type_work', 'wagon_number', 'amount', 'work_date']
        widgets = {
            'type_work': forms.Select(attrs={'class': 'form-control'}),
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
